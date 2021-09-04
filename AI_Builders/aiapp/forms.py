# from django.forms import ModelForm
from app.models import *
from django import forms

TRUE_FALSE_CHOICES = (
	('True','YES'),
	('False','NO'),
	)

class CoursesForm(forms.ModelForm):
	class Meta:
		model=Courses
		fields=['name','sub_name','course_image','price',
				'course_type','author_id','category_id','task_id',
				'total_length_course','slots_available','discount_amount','tax_amount','course_code']
		widgets={
		  	'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
			'sub_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
		  	'course_image': forms.FileInput(attrs={'class': 'form-control','type':'file', 'placeholder': ''}),
		  	'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
		 	'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
		 	# 'is_offer': forms.Select(choices=TRUE_FALSE_CHOICES,attrs={'class': 'form-control', 'placeholder': ''}),
		 	'course_type':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
		 	# 'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'author_id': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'category_id': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'task_id': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            # 'modules': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            # 'miniprojects': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            # 'major_projects': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'total_length_course':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'slots_available':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}),
            # 'slots_remaining':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}),
            # 'joined_slots': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            # 'coupon_discount_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'discount_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'tax_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            # 'total_couponprice_with_tax': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),


		  }


class HelpForm(forms.ModelForm):
	class Meta:
		model=Help
		fields='__all__'
		widgets={
		  	'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
		 	'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
		 	'query':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
		 	'status': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
           

		  }		  

class BootcampForm(forms.ModelForm):
	class Meta:
		model= Bootcamp
		fields= ['image','course_id','task','subject','price','date','status']
		widgets={
			'image': forms.FileInput(attrs={'class': 'form-control','type':'file', 'placeholder': ''}),
			'course_id': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
			'task':forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
			'subject':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
			'price':forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
			'date':forms.DateInput(attrs={'class': 'form-control','type':'date', 'placeholder': ''}),
			'status':forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),





		 }

