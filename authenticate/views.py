import email
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from werkzeug.utils import secure_filename
from . import application
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.core.files.storage import FileSystemStorage
class Cred:
    uname=""
    fname=""
    lname=""
    pass1=""
    tog=False
obj=Cred()

# Create your views here.
def home(request):
    return HttpResponse("Hell")

def signup(request):
    if request.method=="POST":
        obj.uname = request.POST['username']
        obj.fname = request.POST['fname']
        obj.lname = request.POST['lname']
        emai = request.POST['email']
        obj.pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(obj.uname, emai, obj.pass1)
        myuser.first_name = obj.fname
        myuser.last_name = obj.lname
        myuser.save()
        messages.success(request,"Account has been successfully created for "+obj.uname)
        return redirect('signin')
    return render(request,"authenticate/signup.html")

def signin(request):
    if request.method=="POST":
        obj.uname = request.POST['username']
        obj.pass1 = request.POST['pass']
        user=authenticate(username=obj.uname, password=obj.pass1)
        if user is not None:
            obj.tog=True
            login(request,user)
            return redirect("index")
            #return render(request,"site/index.html",{"un":uname})
        else:
            messages.error(request,"Bad credentials!")
            return redirect("signin")
    return render(request,"authenticate/signin.html")

def signout(request):
    obj.tog=False 
    return redirect("signin")

def index(request):
    if obj.tog:
        try:
            if request.method == 'POST':
                f = request.FILES['bt_image']
                filename = str(f.name)
                if filename!='':
                    ext = filename.split(".")
                    if ext[1] in ['png', 'jpg', 'jpeg']:
                        filename = secure_filename(f.name)
                        fs = FileSystemStorage()
                        fs.save(f.name,f)
                        with open("authenticate/static/media/"+filename,'rb') as img:
                            img1=img.name.split('/')[-1]
                            x= application.predict(request,img)
                            x['img'] = img1
                        return render(request,"site/pred.html",x)

        except Exception as e:
            print("Exception\n")
            print(e, '\n')
        
        return render(request,'site/index.html',{"n":obj.uname})
    else:
        return redirect("signin")