from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(task_tb)
admin.site.register(category_tb)
admin.site.register(course_tb)
admin.site.register(Help)
admin.site.register(Bootcamp)
