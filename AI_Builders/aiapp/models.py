from django.db import models

# Create your models here.
class customeruser_tb(models.Model):
	name=models.CharField(max_length=100,default='')
	usertype = models.IntegerField(default=0)
	status = models.BooleanField(default=False)
	phonecode = models.CharField(max_length=100,default='')
	phoneno = models.CharField(max_length=100,default='')
	email=models.CharField(max_length=100,default='')
	password = models.CharField(max_length=100,default='')
	usercode = models.CharField(max_length=100,default='')

	def __str__(self):
		return str(self.name)

class category_tb(models.Model):
	catname=models.CharField(max_length=100,default='')
	catcode =models.CharField(max_length=100,default='')

	def __str__(self):
		return str(self.catname)

class task_tb(models.Model):
	taskname=models.CharField(max_length=100,default='')
	taskcode =models.CharField(max_length=100,default='')

	def __str__(self):
		return str(self.taskname)

class course_tb(models.Model):
	coname=models.CharField(max_length=200,default='')
	cocode =models.CharField(max_length=100,default='')
	cotype =models.CharField(max_length=100,default='')
	cstatus=models.CharField(max_length=100,default='')
	username=models.ForeignKey(customeruser_tb,on_delete=models.CASCADE,related_name="customeruser_username")
	catname=models.ForeignKey(category_tb,on_delete=models.CASCADE,related_name="category_catname")
	taskname=models.ForeignKey(task_tb,on_delete=models.CASCADE,related_name="task_taskname")

	def __str__(self):
		return str(self.coname)

	class Meta:
		db_table = "course_tb"	

class Help(models.Model):
	STATUS_Response = (
        ('Posted', 'Posted'),
        ('Responded', 'Responded')

    )
	name = models.CharField(max_length=500,default='')
	email=models.CharField(max_length=100,default='')
	query = models.CharField(max_length=50000,blank=True,null=True)
	status = models.CharField(max_length=100, default="Posted" ,choices=STATUS_Response, null=True, blank=True)

	def __str__(self):
		return str(self.name)

class Bootcamp(models.Model):
	STATUS = (
		('Next','Next'),
		('Over','Over'),



	)
	image = models.ImageField(upload_to="Bootcamp-image", default='bootcamp.jpg', null=True,
                              blank=True)
	course_id = models.ForeignKey(course_tb, on_delete=models.CASCADE, null=True, blank=True)
	task = models.CharField(max_length=500, null=True, blank=True)
	subject= models.CharField(max_length=500, null=True, blank=True)
	bootcamp_code= models.CharField(max_length=500, null=True, blank=True)
	price = models.FloatField(default=0.0)
	date = models.DateTimeField(null=True,blank=True)
	status = models.CharField(max_length=100, default="Next" ,choices=STATUS, null=True, blank=True)


	def __str__(self):
		return str(self.id)


	

