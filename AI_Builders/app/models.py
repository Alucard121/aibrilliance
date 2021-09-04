from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.apps import apps
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.
class CustomUser(AbstractUser):
    # USERTYPES
    # 0: SUPERADMIN
    # 1: ADMIN
    # 2: CUSTOMER

    usertype = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    phone_code = models.CharField(max_length=2, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    pswd = models.CharField(max_length=100, null=True, blank=True)
    user_code = models.CharField(max_length=500, null=True, blank=True)
    profile_image = models.ImageField(upload_to="Profile-image", default='profile_image.png', null=True,
                                     blank=True)
    position = models.CharField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        db_table = "CustomUser"
class Courses(models.Model):
    COURSE_TYPE_CHOICES = (
        ('Paid', 'Paid'),
        ('Free', 'Free'),

    )
    STATUS_CHOICES = (
        ('Now Active', 'Now Active'),
        ('Up Coming', 'Up Coming'),
        ('Completed', 'Completed'),

    )
    STATUS_DETAILS = (
        ('Completed', 'Completed'),
        ('Next video', 'Next video'),
        ('Removed video', 'Removed video'),
    )
    name = models.CharField(max_length=500,null=True,blank=True)
    sub_name = models.CharField(max_length=500, null=True, blank=True)
    course_image = models.ImageField(upload_to="Course-image", default='course1.jpg', null=True,
                                     blank=True)
    category_id = models.ForeignKey('app.Category', on_delete=models.CASCADE, null=True, blank=True)
    task_id = models.ForeignKey('app.Task', on_delete=models.CASCADE, null=True, blank=True)
    author_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    course_code = models.CharField(max_length=500,null=True,blank=True)
    course_type = models.CharField(max_length=100, choices=COURSE_TYPE_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    price =models.FloatField(default=0.0,null=True, blank=True)
    is_offer =models.BooleanField(default=False,null=True, blank=True)
    credit=models.IntegerField(default=0)
    description=models.CharField(max_length=5000,null=True,blank=True)
    modules = models.ForeignKey('app.Module', on_delete=models.CASCADE, null=True, blank=True)
    miniprojects= models.ForeignKey('app.MiniProject', on_delete=models.CASCADE, null=True, blank=True)
    major_projects= models.ForeignKey('app.MajorProject', on_delete=models.CASCADE, null=True, blank=True)
    total_length_course=models.IntegerField(default=0,null=True, blank=True)
    slots_available=models.IntegerField(default=0,null=True, blank=True)
    slots_remaining = models.IntegerField(default=0,null=True, blank=True)
    joined_slots = models.IntegerField(default=0,null=True, blank=True)
    discount_amount = models.FloatField(default=0.0,null=True, blank=True)
    coupon_discount_amount=models.FloatField(default=0.0,null=True, blank=True)
    tax_amount=models.FloatField(default=0.0,null=True, blank=True)
    total_couponprice_with_tax=models.FloatField(default=0.0,null=True, blank=True)
    batch_id = models.ForeignKey('app.Batches', on_delete=models.CASCADE, null=True, blank=True)
    preview_video = models.FileField(upload_to="Preview_video", null=True, blank=True)
    status = models.CharField(max_length=100, default="Posted", choices=STATUS_DETAILS, null=True, blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True,default=now)
    updated_at = models.DateTimeField(null=True,blank=True)
    deleted_at = models.DateTimeField(null=True,blank=True)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="Courses_createdby")
    updated_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="Courses_updatedby")
    deleted_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="Courses_deletedby")


    def __str__(self):
            return str(self.name)
    class meta:
        db_table = "Courses"
class Module(models.Model):
    course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=500,null=True,blank=True)
    module_code = models.CharField(max_length=500,null=True,blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True,default=now)
    updated_at = models.DateTimeField(null=True,blank=True)
    deleted_at = models.DateTimeField(null=True,blank=True)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="Module_createdby")
    updated_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="Module_updatedby")
    deleted_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="Module_deletedby")


    def __str__(self):
            return str(self.name)
    class meta:
        db_table = "Module"
class MiniProject(models.Model):
    course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=500,null=True,blank=True)
    mini_project_code = models.CharField(max_length=500,null=True,blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True,default=now)
    updated_at = models.DateTimeField(null=True,blank=True)
    deleted_at = models.DateTimeField(null=True,blank=True)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="MiniProject_createdby")
    updated_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="MiniProject_updatedby")
    deleted_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="MiniProject_deletedby")


    def __str__(self):
            return str(self.name)
    class meta:
        db_table = "MiniProject"
class MajorProject(models.Model):
    course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=500,null=True,blank=True)
    major_project_code = models.CharField(max_length=500,null=True,blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True,default=now)
    updated_at = models.DateTimeField(null=True,blank=True)
    deleted_at = models.DateTimeField(null=True,blank=True)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="MajorProject_createdby")
    updated_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="MajorProject_updatedby")
    deleted_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="MajorProject_deletedby")


    def __str__(self):
            return str(self.name)
    class meta:
        db_table = "MajorProject"
class Category(models.Model):

    name = models.CharField(max_length=500,null=True,blank=True)
    category_code = models.CharField(max_length=500,null=True,blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True,default=now)
    updated_at = models.DateTimeField(null=True,blank=True)
    deleted_at = models.DateTimeField(null=True,blank=True)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="Category_createdby")
    updated_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="Category_updatedby")
    deleted_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="Category_deletedby")


    def __str__(self):
            return str(self.name)
    class meta:
        db_table = "Category"


class Task(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    task_code = models.CharField(max_length=500, null=True, blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Task_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Task_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Task_deletedby")

    def __str__(self):
        return str(self.name)

    class meta:
        db_table = "Task"
class Bootcamp(models.Model):
    STATUS = (
        ('Next', 'Next'),
        ('Over', 'Over')

    )
    name = models.CharField(max_length=500, null=True, blank=True)
    sub_name = models.CharField(max_length=500, null=True, blank=True)

    image = models.ImageField(upload_to="Bootcamp-image", default='bootcamp.jpg', null=True,
                              blank=True)
    course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey('app.Task', on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=500, null=True, blank=True)
    bootcamp_code= models.CharField(max_length=500, null=True, blank=True)
    price = models.FloatField(default=0.0)
    date = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=100, default="Next" ,choices=STATUS, null=True, blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Bootcamp_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Bootcamp_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Bootcamp_deletedby")
    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "Bootcamp"
class Help(models.Model):
    STATUS_Response = (
        ('Posted', 'Posted'),
        ('Responded', 'Responded')

    )
    name = models.CharField(max_length=500, null=True, blank=True)
    email =models.EmailField(null=True, blank=True)
    query =models.CharField(max_length=5000,blank=True,null=True)
    status = models.CharField(max_length=100, default="Posted" ,choices=STATUS_Response, null=True, blank=True)

    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Help_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Help_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Help_deletedby")
    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "Help"

class Batches(models.Model):
    STATUS_BATCHES = (
        ('Removed', 'Removed'),
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed')

    )
    course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)
    batch_name= models.CharField(max_length=500, null=True, blank=True)
    starting_date = models.DateTimeField(null=True,blank=True)
    ending_date = models.DateTimeField(null=True,blank=True)
    batch_slots_remaining= models.IntegerField(default=0, null=True, blank=True)
    joined_batch_slots= models.IntegerField(default=0, null=True, blank=True)
    total_batch_slots= models.IntegerField(default=0, null=True, blank=True)
    available_slots= models.IntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=100, default="Posted" ,choices=STATUS_BATCHES, null=True, blank=True)
    price = models.FloatField(default=0.0)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Batches_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Batches_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Batches_deletedby")
    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "Batches"
class Payment(models.Model):
    STATUS_PAYMENT = (
        ('Paid', 'Paid'),
        ('Not Paid', 'Not Paid'),
         )
    # course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)
    # batch_id = models.ForeignKey('app.Batches', on_delete=models.CASCADE, null=True, blank=True)
    Order_summary=models.ForeignKey('app.Order_summary', on_delete=models.CASCADE, null=True, blank=True)

    coupon = models.CharField(max_length=500, null=True, blank=True)
    total_price = models.FloatField(default=0.0)
    coupon_discount_price = models.FloatField(default=0.0)
    tax_amount = models.FloatField(default=0.0)
    total_including_task= models.FloatField(default=0.0)
    paid_amount = models.FloatField(default=0.0)
    balance_amount = models.FloatField(default=0.0)
    paypal_status=models.CharField(max_length=500, null=True, blank=True)
    message_from_paypal=models.CharField(max_length=500, null=True, blank=True)
    payment_id=models.CharField(max_length=500, null=True, blank=True)
    payment_date=models.DateTimeField(null=True,blank=True)
    payment_details=models.CharField(max_length=5000, null=True, blank=True)
    payment_person=models.CharField(max_length=500, null=True, blank=True)
    payment_error_message=models.CharField(max_length=500, null=True, blank=True)
    payment_success_message=models.CharField(max_length=500, null=True, blank=True)
    currency_code=models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=100, default="Posted" ,choices=STATUS_PAYMENT, null=True, blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Payment_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Payment_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Payment_deletedby")


    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "Payment"
class Order_summary(models.Model):
    STATUS_PAYMENT = (
        ('Paid', 'Paid'),
        ('Not Paid', 'Not Paid'),
    )
    course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)
    batch_id = models.ForeignKey('app.Batches', on_delete=models.CASCADE, null=True, blank=True)
    order_date=models.DateTimeField(null=True,blank=True)
    order_person= models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, default="Posted" ,choices=STATUS_PAYMENT, null=True, blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Order_summary_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Order_summary_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Order_summary_deletedby")
    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "Order_summary"
class CoursesDetails(models.Model):
    STATUS_DETAILS = (
        ('Completed', 'Completed'),
        ('Next video', 'Next video'),
        ('Removed video', 'Removed video'),
    )
    course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)
    batch_id = models.ForeignKey('app.Batches', on_delete=models.CASCADE, null=True, blank=True)
    preview_video = models.FileField(upload_to="Preview_video",  null=True,blank=True)
    status = models.CharField(max_length=100, default="Posted" ,choices=STATUS_DETAILS, null=True, blank=True)
    date=models.DateTimeField(null=True,blank=True)

    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="CoursesDetails_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="CoursesDetails_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="CoursesDetails_deletedby")

    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "CoursesDetails"
class Literature(models.Model):
    TYPE = (
        ('Webinar', 'Webinar'),
        ('Podcast', 'Podcast'),
        ('Blog', 'Blog'),
        ('Article', 'Article'),
    )
    STATUS = (
        ('Completed', 'Completed'),
        ('Next', 'Next'),
        ('Removed', 'Removed'),
    )
    name= models.CharField(max_length=500, null=True, blank=True)
    views= models.IntegerField(default=0, null=True, blank=True)
    likes= models.IntegerField(default=0, null=True, blank=True)
    tags= models.CharField(max_length=500, null=True, blank=True)
    image= models.ImageField(upload_to="Literature-image", default='profile_image.png', null=True,
                                     blank=True)
    type_of_literature= models.CharField(max_length=100,  choices=TYPE, null=True, blank=True)
    author_id= models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,related_name="author")
    course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)
    batch_id = models.ForeignKey('app.Batches', on_delete=models.CASCADE, null=True, blank=True)
    about= models.CharField(max_length=5000, null=True, blank=True)
    time= models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    team_members=models.ManyToManyField(CustomUser,related_name="team_members")
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Literature_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Literature_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Literature_deletedby")
    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "Literature"
class Comments(models.Model):
    literature_id = models.ForeignKey('app.Literature', on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    comments=models.CharField(max_length=5000, null=True, blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    responted_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "Comments"

class Events(models.Model):
    STATUS = (
        ('Completed', 'Completed'),
        ('Live Now', 'Live Now'),
        ('Next', 'Next'),
        ('Removed', 'Removed'),
    )
    status = models.CharField(max_length=100, choices=STATUS, null=True, blank=True)
    teachers=models.ManyToManyField(CustomUser,related_name="teachers")
    course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)
    tags = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to="Events-image", default='profile_image.png', null=True,
                              blank=True)
    about= models.CharField(max_length=5000, null=True, blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    main_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,related_name="main_person")
    lenghth_to_conduct= models.IntegerField(default=0, null=True, blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Events_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Events_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="Events_deletedby")
    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "Events"
class CourseMembers(models.Model):
    STATUS = (
        ('Paid', 'Paid'),
        ('Not Paid', 'Not Paid'),

    )
    course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    about_user=models.CharField(max_length=5000,null=True,blank=True)
    user_account = models.CharField(max_length=100, choices=STATUS, null=True, blank=True)
    total_amount = models.FloatField(default=0.0)

    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="CourseMembers_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="CourseMembers_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="CourseMembers_deletedby")
    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "CourseMembers"
        
class Webinar(models.Model):
    STATUS = (
        ('Completed', 'Completed'),
        ('Live Now', 'Live Now'),
        ('Next', 'Next'),
        ('Removed', 'Removed'),
    )
    name= models.CharField(max_length=500, null=True, blank=True)

    course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)
    literature_id = models.ForeignKey('app.Literature', on_delete=models.CASCADE, null=True, blank=True)
    about = models.CharField(max_length=5000, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True, blank=True)
    team_members=models.ManyToManyField(CustomUser,related_name="webinarteam_members")
    image = models.ImageField(upload_to="webinar-image", default='profile_image.png', null=True,
                              blank=True)
    webinar_link = models.CharField(max_length=500, null=True, blank=True)
    webinar_code=models.CharField(max_length=500, null=True, blank=True)

    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="webinar_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="webinar_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="webinar_deletedby")

    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "Webinar"
class CoursesTopics(models.Model):

    course_id = models.ForeignKey('app.Courses', on_delete=models.CASCADE, null=True, blank=True)
    batch_id = models.ForeignKey('app.Batches', on_delete=models.CASCADE, null=True, blank=True)
    status=models.BooleanField(default=True)
    topic_name=models.CharField(max_length=5000, null=True, blank=True)
    about_topic=models.CharField(max_length=5000, null=True, blank=True)
    date=models.DateTimeField(null=True,blank=True)
    topic_order=models.IntegerField(default=0)
    important_topic=models.BooleanField(default=False)
    special_topic=models.BooleanField(default=False)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="CoursesTopics_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="CoursesTopics_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="CoursesTopics_deletedby")

    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "CoursesTopics"
class CoursesTopicsDetails(models.Model):

    topic_id = models.ForeignKey('app.CoursesTopics', on_delete=models.CASCADE, null=True, blank=True)
    sub_topic_name = models.CharField(max_length=5000, null=True, blank=True)
    video = models.FileField(upload_to="topic_video",  null=True,blank=True)
    status = models.BooleanField(default=True)
    date=models.DateTimeField(null=True,blank=True)
    details=models.CharField(max_length=5000, null=True, blank=True)
    pdf=models.FileField(upload_to="topic_pdf",  null=True,blank=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="CoursesTopicsDetails_createdby")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="CoursesTopicsDetails_updatedby")
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="CoursesTopicsDetails_deletedby")

    def __str__(self):
        return str(self.id)

    class meta:
        db_table = "CoursesTopicsDetails"
def operation(model_name,created,instance,default_key,field_name):
    model = apps.get_model('app', model_name)

    if created:
        code = default_key  + uuid.uuid4().hex[:4]
        code_upper = code.upper()
        update = model.objects.filter(id=instance.id).update(**{field_name: code_upper})
    else:
        # update = model.objects.filter(id=instance.id).update(customer_code=instance.customer_code)
        pass
@receiver(post_save, sender=CustomUser)
def create_customer_code(sender, instance, created, **kwargs):
    model_name="CustomUser"
    default_key ="usr"
    field_name = "user_code"
    d=operation(model_name,created,instance,default_key,field_name)
@receiver(post_save, sender=Task)
def create_task_code(sender, instance, created, **kwargs):
    model_name="Task"
    default_key ="tsk"
    field_name = "task_code"
    d=operation(model_name,created,instance,default_key,field_name)
@receiver(post_save, sender=Category)
def create_task_code(sender, instance, created, **kwargs):
    model_name="Category"
    default_key ="ctr"
    field_name = "category_code"
    d=operation(model_name,created,instance,default_key,field_name)
@receiver(post_save, sender=Bootcamp)
def create_task_code(sender, instance, created, **kwargs):
    model_name="Bootcamp"
    default_key ="btc"
    field_name = "bootcamp_code"
    d=operation(model_name,created,instance,default_key,field_name)
