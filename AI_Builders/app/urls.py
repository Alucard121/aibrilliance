"""AI_Build URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .Views.apiView import *
from .Views.webView import *

from django.views.generic import TemplateView
urlpatterns = [
    path('myadmin/index',index),



    path('api/signup', UserSave.as_view(), name='UserSave'),
    path('api/login', Login.as_view(), name='login'),
    path('api/send/otp', verify_otp.as_view(), name='verify_otp'),
    path('api/verify/otp/input', verify_otp_input.as_view(), name='verify_otp_input'),
    path('api/forgot/password', ForgotPassword.as_view(), name='ForgotPassword'),

    path('api/courses/list', getCoursesList.as_view(), name='getCoursesList'),
    path('api/courses/details/list', getCoursesDetailsList.as_view(), name='getCoursesDetailsList'),
    path('api/course/topics/list', getCourseTopicList.as_view(), name='getCourseTopicList'),

    path('api/category/list', getCategoryList.as_view(), name='getCategoryList'),

    path('api/task/list', getTaskList.as_view(), name='getTaskList'),

    path('api/bootcamp/list', getBootcampList.as_view(), name='getBootcampList'),

    path('api/help', HelpSave.as_view(), name='HelpSave'),

    path('api/webinar/list', getWebinarList.as_view(), name='getWebinarList'),

]
