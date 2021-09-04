from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Courses)
admin.site.register(Task)
admin.site.register(Category)
admin.site.register(Bootcamp)
admin.site.register(Help)
admin.site.register(Webinar)
admin.site.register(CoursesTopics)

admin.site.register(CoursesTopicsDetails)