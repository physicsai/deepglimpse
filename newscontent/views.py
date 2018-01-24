from newscontent.models import Newscontent

from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404, reverse, Http404
from newscontent.forms import ContactForm    
from django.core.mail import send_mail, get_connection
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import UserCreationForm
from newscontent.forms import CustomUserCreationForm
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from newscontent.helpers import generate_activation_key
from newscontent.models import SiteUser, ZipCodes

def save_session_data(request):
	# set new data
	request.session['id'] = 1
	request.session['name'] = 'root'
	request.session['password'] = 'rootpass'
	return HttpResponse("Session Data Saved")


def access_session_data(request):
	response = ""
	if request.session.get('id'):
		response += "Id : {0} <br>".format(request.session.get('id'))
	if request.session.get('name'):
		response += "Name : {0} <br>".format(request.session.get('name'))
	if request.session.get('password'):
		response += "Password : {0} <br>".format(request.session.get('password'))

	if not response:
		return HttpResponse("No session data")
	else:
		return HttpResponse(response)


def delete_session_data(request):
	try:
		del request.session['id']
		del request.session['name']
		del request.session['password']
	except KeyError:
		pass

	return HttpResponse("Session Data cleared")

def test_session(request):
	request.session.set_test_cookie()
	return HttpResponse("Testing session cookie")


def test_delete(request):
	if request.session.test_cookie_worked():
		request.session.delete_test_cookie()
		response = HttpResponse("Cookie test passed")
	else:
		response = HttpResponse("Cookie test failed")
	return response

def stop_tracking(request):
	if request.COOKIES.get('visits'):
	   response = HttpResponse("Cookies Cleared")
	   response.delete_cookie("visits")
	else:
		response = HttpResponse("We are not tracking you.")
	return response

def track_user(request):
	response = render(request, 'newscontent/track_user.html') # store the response in response variable
	if not request.COOKIES.get('visits'):        
		response.set_cookie('visits', '1', 3600 * 24 * 365 * 2)
	else:
		visits = int(request.COOKIES.get('visits', '1')) + 1
		response.set_cookie('visits', str(visits),  3600 * 24 * 365 * 2)
	return response

def test_cookie(request):   
	if not request.COOKIES.get('color'):
		response = HttpResponse("Cookie Set")
		response.set_cookie('color', 'blue')
		return response
	else:
		return HttpResponse("Your favorite color is {0}".format(request.COOKIES['color']))

def display_meta(request):
	values = request.META   
	html = []
	for k in sorted(values):
		html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, values[k]))
	return HttpResponse('<table>%s</table>' % '\n'.join(html))


########################################################
########################################################

# def register(request):
#     if request.method == 'POST':
#         f = CustomUserCreationForm(request.POST)
#         if f.is_valid():
#             f.save()
#             messages.success(request, 'Account created successfully')
#             return redirect('register')

#     else:
#         f = CustomUserCreationForm()

#     return render(request, 'newscontent/register.html', {'form': f})

def register(request):
	auth.logout(request)
	if request.method == 'POST':
		f = CustomUserCreationForm(request.POST)
		if f.is_valid():

			# send email verification now

			activation_key = generate_activation_key(username=request.POST['username'])

			subject = "DeepGlimpse Account Verification"

			message = '''\n
Please visit the following link to verify your account \n\n{0}://{1}/activate/account/?key={2}
						'''.format(request.scheme, request.get_host(), activation_key)            

			error = False

			try:
				con = get_connection('django.core.mail.backends.console.EmailBackend')
				send_mail(subject, message, 'noreply@example.com', [request.POST['email']],connection=con)
				messages.add_message(request, messages.INFO, 'Account created! Click on the link sent to your email to activate the account')

			except:
			    error = True
			    messages.add_message(request, messages.INFO, 'Unable to send email verification. Please try again')

			if not error:
				u = User.objects.create_user(
						request.POST['username'],
						request.POST['email'],
						request.POST['password1'],
						is_active = 0
				)

				siteuser = SiteUser()
				siteuser.activation_key = activation_key
				siteuser.activation_key2= activation_key
				siteuser.zipper = request.POST['zipper']
				# print(siteuser.zip_code)
				# print(type(siteuser.zip_code))
				siteuser.user = u
				siteuser.save()

			return redirect('register')

	else:
		f = CustomUserCreationForm()

	return render(request, 'newscontent/register.html', {'form': f})

def activate_account(request):
	key = request.GET['key']
	if not key:
		raise Http404()

	r = get_object_or_404(SiteUser, activation_key=key, email_validated=False)
	r.user.is_active = True
	r.user.save()
	r.email_validated = True
	r.save()

	return render(request, 'newscontent/activated.html')




def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/user_home/')
	# else:
	# 	auth.logout(request)

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username, password=password)

		if user is not None:
			# correct username and password login the user
			auth.login(request, user)
			return HttpResponseRedirect('/user_home/')

		else:
			messages.error(request, 'Error wrong username/password')

	return render(request, 'newscontent/login.html')


def logout(request):
	auth.logout(request)
	return render(request,'newscontent/logout.html')


def user_home(request):
	if not request.user.is_authenticated():
		return redirect('/login/')
	# print(request.user)
	try:
		r = get_object_or_404(SiteUser,user=request.user)
	except:
		return HttpResponseRedirect('/register/')


	zip_code = r.zipper
	#take first matching ZIP object:
	try:
		first_matching_zip = ZipCodes.objects.filter(zipcode=str(int(zip_code)))[0]
		my_city = first_matching_zip.city
	except:
		my_city = "ZIP code lookup failed!"
	
	# print(dir(r))
	print(r.user.is_active)
	print(r.user_id)
	print(r.activation_key)
	print(r.email_validated)
	# print(type(request.user))
	# print(dir(request.user))
	# print('\n')
	# print(request.user.username)
	return render(request, 'newscontent/user_home.html',{'zip_code':zip_code,'my_city':my_city})

def search(request):
	error = False
	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			error = True
		else:
			content = Newscontent.objects.filter(title__icontains=q)
			return render(request, 'newscontent/search_results.html',
					  {'content': content, 'query': q})
	return render(request, 'newscontent/search_form.html', {'error': error})