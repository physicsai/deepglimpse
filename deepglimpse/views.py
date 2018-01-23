from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.shortcuts import render, redirect, get_object_or_404, reverse, Http404
from django.core.mail import send_mail, get_connection
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import UserCreationForm
# from .forms import CustomUserCreationForm
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
# from .helpers import generate_activation_key
# from .models import SiteUser





########################################################
########################################################

def hello(request):
	return HttpResponse("Hello world")


def current_datetime(request):
	now = datetime.datetime.now()
	return render(request, 'current_datetime.html', {'current_date': now})

def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	return render(request, 'hours_ahead.html', {'hour_offset': offset,'next_time':dt})




def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			con = get_connection('django.core.mail.backends.console.EmailBackend')
			send_mail(
				cd['subject'],
				cd['message'],
				cd.get('email', 'noreply@example.com'),
				['siteowner@example.com'],
				connection=con
			)
			return HttpResponseRedirect('/contact/thanks/')
	else:
		form = ContactForm(
			initial={'subject': 'I love your site!'}
		)

	return render(request, 'contact_form.html', {'form': form})

def thanks(request):
	return render(request, 'thanks_form.html')
