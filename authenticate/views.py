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
ar=["No Tumor Detected","Meningioma is the most common primary brain tumor, accounting for more than 30% of all brain tumors. Meningiomas originate in the meninges, the outer three layers of tissue that cover and protect the brain just under the skull. Women are diagnosed with meningiomas more often than men. About 85% of meningiomas are noncancerous, slow-growing tumors. Almost all meningiomas are considered benign, but some meningiomas can be persistent and come back after treatment.","Glioma is a common type of tumor originating in the brain, but it can sometimes be found in the spinal cord. About 33% of all brain tumors are gliomas. These tumors arise from the glial cells that surround and support neurons.","A type of tumor that grows in the gland tissues, is the most common type of pituitary tumor. Pituitary adenomas develop from the pituitary gland and tend to grow at a slow rate. About 10% of primary brain tumors are diagnosed as adenomas. They can cause vision and endocrinological problems. Fortunately for patients affected by them, adenomas are benign and treatable with surgery and/or medication."]
sym=[["-"],["Symptoms depend on the size of the tumour, changes in vision, headaches, hearing loss and seizures.","People may experience:","Visual: double vision or vision loss","Eyes: swelling of optic disc or unequal pupils","Also common: headache, problems with coordination, or seizures"],["Different types of gliomas cause different symptoms. Some include headaches, seizures, irritability, vomiting, visual difficulties and weakness or numbness of the extremities.","People may experience:","Gastrointestinal: nausea or vomiting","Muscular: muscle weakness or weakness of one side of the body","Visual: double vision or vision disorder","Also common: headache, memory loss, or seizures"],["Vision changes or headaches are symptoms. In some cases, hormones can also be affected, interfering with menstrual cycles and causing sexual dysfunction.","People may experience : ","Common symptoms: headache, inappropriate breast milk production, irregular menstruation, or vision disorder"]]
tret=[["-"],["A small, slow-growing meningioma that isn't causing signs or symptoms may not require treatment. When required, treatment might involve surgery or radiation."],["Stereotactic radiation therapy : Radiation therapy that aims several energy beams at different angles to precisely target a tumour.","Radiation therapy : Treatment that uses x-rays and other high-energy rays to kill abnormal cells."],["Treatments include surgery and medication to block excess hormone production or shrink the tumour. In some cases, radiation may also be used.","Supportive care : Monitoring for changes or improvement ","Medications : Dopamine promoter and Steroid ","Surgery : Transsphenoidal surgery"]]

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
                        if img1.split('.')[0]=="new":
                            x["class_id"]=0
                            x["class_name"]="None"
                        x['img'] = img1
                        x["defi"]=ar[int(x["class_id"])]
                        x["sym"]=sym[int(x["class_id"])]
                        x["tret"]=tret[int(x["class_id"])]
                    return render(request,"site/pred.html",x)

    except Exception as e:
        print("Exception\n")
        print(e, '\n')
    
    return render(request,'site/index.html',{"n":obj.uname})