from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import *
from .forms import *
from app.models import *

# Create your views here.

def home(request):
	
	return render (request,'home.html')

def index(request):
	
	return render (request,'index.html')

def register(request):
	if request.method=='POST':
		name=request.POST['name'] 
		# usertype=request.POST['usertype'] 
		# status=request.POST['status']
		# phonecode=request.POST['phonecode']
		phoneno=request.POST['phoneno']
		email=request.POST['email']
		password=request.POST['password']
		# usercode=request.POST['usercode']
		var1=CustomUser.objects.filter(username=name,email=email,password=password)
		if var1:
			  return render(request,'register.html')
		else:
			a=CustomUser(username=name,email=email,password=password)
			a.save()
			return render(request,'login.html')
	else:
		return render(request,'register.html') 		

	
	return render (request,'register.html')	

def login(request):
	if request.method=='POST':
		
		email=request.POST['email']
		password=request.POST['password']
		query=CustomUser.objects.filter(email=email,password=password)
		if query:
			for x in query:
				
				request.session['userid']=x.id     
				request.session['username']=x.username
				return render(request,'index.html')
		else:
			return render(request,'login.html') 
	else:
		return render(request,'login.html')			

def logout(request):
	del request.session['userid']
	del request.session['username']
	return render(request,'register.html')

def category(request):
	if request.method=='POST':
		name=request.POST['name']
		category_code=request.POST.get('category_code')
		var2=Category.objects.filter(name=name)
		if var2:
			  return render(request,'category.html')
		else:
			c=Category(name=name)
			c.save()
			print(c)
			return HttpResponseRedirect("/categorylist/")
	else:
		return render(request,'category.html') 		

	
	return render (request,'category.html')	

def task(request):
	if request.method=='POST':
		name=request.POST['name']
		task_code=request.POST.get('task_code')
		var3=Task.objects.filter(name=name)
		if var3:
			return render(request,'task.html')
		else:
			t=Task(name=name)
			t.save()
			print(t)
			return redirect('/tasklist/')
	else:
		return render(request,'task.html') 		

	
	return render(request,'task.html')	

# def addcourse(request):
# 	if request.method=='POST':
# 		coname = request.POST.get("coname")
# 		cocode = request.POST.get("cocode")
# 		cotype = request.POST.get("cotype")
# 		cstatus = request.POST.get("cstatus")
# 		nameid = request.POST.get("name")
# 		nameid=request.POST.get("name")
# 		usernameid=request.POST.get("username")
# 		name=Task.objects.get(id=nameid)
# 		name=Category.objects.get(id=nameid)
# 		username=customeruser_tb.objects.get(id=usernameid)
# 		Courses.objects.create(coname=coname,cocode=cocode,cotype=cotype,cstatus=cstatus,name=name,name=name,username=username)
		
# 	return render(request,"addcourse.html",{'names':Task.objects.all(),'names':Category.objects.all(),'usernames':customeruser_tb.objects.all()})

	# else:
	# 	return render(request,"addcourse.html",{'names':Task.objects.all(),'names':Category.objects.all(),'usernames':customeruser_tb.objects.all()})
			

def courselist(request):
	
	coulist=Courses.objects.all()
	return render(request,'courselist.html',{'coulist':coulist})

def coursefind(request):
	s=Courses.objects.get(pk=request.GET["a"])
	return render(request,"coursefind.html",{"x":s})

# def courseupdate(request):


	# s=Courses.objects.get(pk=request.POST["txtid"])
	# s.coname=request.POST["coname"]
	# s.cocode=request.POST["cocode"]
	# s.cotype=request.POST["cotype"]
	# s.cstatus=request.POST["cstatus"]
	# s.nameid=request.POST["name"]
	# s.nameid=request.POST["name"]
	# s.usernameid=request.POST["username"]
	
	
	
	# s.save()
	
	# return redirect("/courselist/")	

def createcourse(request):
	form=CoursesForm()
	if request.method =='POST':
		
		form = CoursesForm(request.POST,request.FILES)
		if form.is_valid():
			form = form.save(commit=False)
			form.status="Now Active"
			form.save()
			print("yes")
			return redirect('/courselist/')
		else:
			print("hhhhh",form.errors)
	content = {'form':form}
	return render(request,'courseform.html',content)

def updatecourse(request,pk):

	course=Courses.objects.get(id=pk)
	form = CoursesForm(instance=course)
	if request.method =='POST':
		
		form = CoursesForm(request.POST,request.FILES,instance=course)
		if form.is_valid():
			form.save()
			return redirect('/courselist/')

	context =  {'form':form}	
	return render(request,'courseform.html',context)


def coursedelete(request):
	c=request.GET["cid"]
	Courses.objects.all().filter(id=c).delete()
	return HttpResponseRedirect("/courselist/")	


	
def categorylist(request):
	
	catlist=Category.objects.all().filter
	return render(request,'categorylist.html',{'catlist':catlist})	


def catedit(request):
	s=Category.objects.get(pk=request.GET["a"])
	return render(request,"catedit.html",{"x":s})

def catupdate(request):
	s=Category.objects.get(pk=request.POST["txtid"])
	s.name=request.POST["name"]
	# s.category_code=request.POST["category_code"]
	s.save()
	print(s)
	return redirect("/categorylist/")	

def catdelete(request):
	c=request.GET["cid"]
	Category.objects.all().filter(id=c).delete()
	return HttpResponseRedirect("/categorylist/")



def tasklist(request):
	
	tasklist=Task.objects.all().filter
	return render(request,'tasklist.html',{'tasklist':tasklist})

def taskedit(request):
	s=Task.objects.get(pk=request.GET["a"])
	return render(request,"taskedit.html",{"x":s})

def taskupdate(request):
	s=Task.objects.get(pk=request.POST["txtid"])
	s.name=request.POST["name"]
	# s.task_code=request.POST["task_code"]
	s.save()
	
	return redirect("/tasklist/")			

def taskdelete(request):
	c=request.GET["cid"]
	Task.objects.all().filter(id=c).delete()
	return HttpResponseRedirect("/tasklist/")	

def createhelp(request):
	form=HelpForm()
	if request.method =='POST':
		
		form = HelpForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/helplist/')
	content = {'form':form}
	return render(request,'helpform.html',content)

def helplist(request):
	
	helplist=Help.objects.all().filter
	return render(request,'helplist.html',{'helplist':helplist})

def updatehelp(request,pk):

	helps=Help.objects.get(id=pk)
	form = HelpForm(instance=helps)
	if request.method =='POST':
		
		form = HelpForm(request.POST,instance=helps)
		if form.is_valid():
			form.save()
			return redirect('/helplist/')

	context =  {'form':form}	
	return render(request,'helpform.html',context)

def helpdelete(request):
	c=request.GET["cid"]
	Help.objects.all().filter(id=c).delete()	
	return HttpResponseRedirect("/helplist/")	

def createboot(request):
	form=BootcampForm()
	if request.method =='POST':
		
		form =BootcampForm(request.POST,request.FILES)

		if form.is_valid():
			form=form.save(commit=False)
			form.created_by=request.user
			form.save()
		else:
			print(form.errors)

		return redirect('/bootlist/')
	content = {'form':form}
	return render(request,'bootform.html',content)	

def bootlist(request):
	
	bootlist=Bootcamp.objects.all().filter
	return render(request,'bootlist.html',{'bootlist':bootlist})	
		
def updateboot(request,pk):

	boot=Bootcamp.objects.get(id=pk)
	form = BootcampForm(instance=boot)
	if request.method =='POST':
		
		form = BootcampForm(request.POST,request.FILES,instance=boot)
		if form.is_valid():
			# form.date=datetime.datetime.now().date()
			form.save()
		return redirect('/bootlist/')

	context =  {'form':form,'boot':boot}	
	return render(request,'bootedit.html',context)

def bootdelete(request):
	c=request.GET["cid"]
	Bootcamp.objects.all().filter(id=c).delete()	
	return HttpResponseRedirect("/bootlist/")	


