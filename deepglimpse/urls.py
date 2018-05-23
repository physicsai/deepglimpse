"""deepglimpse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from deepglimpse.views import hello, current_datetime, hours_ahead, contact, thanks


urlpatterns = [
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^admin/', admin.site.urls),
    url(r'^hello/$', hello),
    # url(r'^register/$', register, name='register'),
    url(r'^time/$', current_datetime),
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
    url(r'^contact/$', contact),
    url(r'^contact/thanks/$', thanks),
    url(r'^', include('newscontent.urls', namespace='newscontent')),
    url(r'^chat/', include('chat.urls')),

]
