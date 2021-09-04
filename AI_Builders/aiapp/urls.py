from django.urls import path
from aiapp import views


urlpatterns=[
path('',views.home),
path('index/',views.index),
path('register/',views.register),
path('login/',views.login),
path('logout/',views.logout),
path('category/',views.category,name="create_category"),
path('categorylist/',views.categorylist),
path('catdelete/',views.catdelete),
path('catedit/',views.catedit),
path('catupdate/',views.catupdate),
path('task/',views.task,name="create_task"),
path('tasklist/',views.tasklist),
path('taskdelete/',views.taskdelete),
path('taskedit/',views.taskedit),
path('taskupdate/',views.taskupdate),
# path('addcourse/',views.addcourse),
path('courselist/',views.courselist),
path('coursefind/',views.coursefind),
# path('courseupdate/',views.courseupdate),
path('coursedelete/',views.coursedelete),
path('create_course/',views.createcourse ,name="create_course"),
path('update_course/<str:pk>/',views.updatecourse ,name="update_course"),
path('create_help/',views.createhelp ,name="create_help"),
path('helplist/',views.helplist),
path('update_help/<str:pk>/',views.updatehelp ,name="update_help"),
path('helpdelete/',views.helpdelete),
path('create_boot/',views.createboot ,name="create_boot"),
path('bootlist/',views.bootlist),
path('update_boot/<str:pk>/',views.updateboot ,name="update_boot"),
path('bootdelete/',views.bootdelete),







]