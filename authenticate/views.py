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

# Create your views here.
def home(request):
    return HttpResponse("Hell")

def signup(request):
    if request.method=="POST":
        uname = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        emai = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(uname, emai, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Account has been successfully created for "+uname)
        return redirect('signin')
    return render(request,"authenticate/signup.html")

def signin(request):
    if request.method=="POST":
        uname = request.POST['username']
        pas = request.POST['pass']
        user=authenticate(username=uname, password=pas)
        if user is not None:
            login(request,user)
            return redirect("index")
            #return render(request,"site/index.html",{"un":uname})
        else:
            messages.error(request,"Bad credentials!")
            return redirect("signin") 

    return render(request,"authenticate/signin.html")

def index(request):
    
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
    return render(request,'site/index.html')