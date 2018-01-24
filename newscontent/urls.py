from newscontent import views
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
# from deepglimpse.views import hello, current_datetime, hours_ahead, contact, thanks


urlpatterns = [
    url(r'^search/$', views.search),
    url(r'^meta/$', views.display_meta),
	url(r'^password-change-done/$',auth_views.password_change_done,{'template_name': 'password_change_done.html'},name='password_change_done'),
    url(r'^password-change/$',auth_views.password_change,{'template_name': 'password_change.html','post_change_redirect': 'password_change_done'},name='password_change'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^user_home/$', views.user_home, name='user_home'),
    url(r'^cookie/$', views.test_cookie, name='cookie'),
    url(r'^track_user/$', views.track_user, name='track_user'),
    url(r'^stop-tracking/$', views.stop_tracking, name='stop_tracking'),
    url(r'^test-delete/$', views.test_delete, name='test_delete'),
    url(r'^test-session/$', views.test_session, name='test_session'),
    url(r'^save-session-data/$', views.save_session_data, name='save_session_data'),
    url(r'^access-session-data/$', views.access_session_data, name='access_session_data'),
    url(r'^delete-session-data/$', views.delete_session_data, name='delete_session_data'),
    url(r'^register/$', views.register, name='register'),
    url(r'^activate/account/$', views.activate_account, name='activate'),

]