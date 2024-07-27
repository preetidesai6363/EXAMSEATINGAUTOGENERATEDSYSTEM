from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentLoginForm
from adminapp.models import AddStudent, AdminAnnounce, Examallotment

# templates
STUDENTLOGINPAGE = "studentlogin.html"
STUDENTHOMEPAGE = "studenthome.html"
VIEWSTUDENTPROFILEPAGE = "viewstudentprofile.html"
STUDENTANNOUNCEMENTPAGE = "studentannouncement.html"
STUDENTEXAMDETAILSPAGE = "studentexamdetails.html"
RESETSTUDENTPASSWORDPAGE = "resetstudentpassword.html"
# Create your views here.


def studentlogin(req):
    context = {}
    context['form'] = StudentLoginForm()
    if req.method == "POST":
        form = StudentLoginForm(req.POST)
        if form.is_valid():
            Studentemail = form.cleaned_data['Studentemail']
            Studentpassword = form.cleaned_data['Studentpassword']
            print(Studentemail, Studentpassword)
            dc = AddStudent.objects.filter(
                email=Studentemail, password=Studentpassword).exists()
            if dc:
                req.session['studentemail'] = Studentemail
                return render(req, STUDENTHOMEPAGE)

    return render(req, STUDENTLOGINPAGE, context)


def viewstudentprofile(req):
    student_profile = AddStudent.objects.filter(
        email=req.session['studentemail'])
    return render(req, VIEWSTUDENTPROFILEPAGE, {'student_profile': student_profile})


def studentannouncement(req):
    all_messages = AdminAnnounce.objects.all()
    return render(req, STUDENTANNOUNCEMENTPAGE, {'all_messages': all_messages})


def studentexamdetails(req):
    data = Examallotment.objects.filter(
        Student_Email=req.session['studentemail'])
    return render(req, STUDENTEXAMDETAILSPAGE, {'data': data})


def resetstudentpassword(req):
    if req.method == "POST":
        old_password = req.POST['oldpassword']
        data = AddStudent.objects.filter(
            email=req.session['studentemail'], password=old_password).exists()
        if data:
            return render(req, RESETSTUDENTPASSWORDPAGE, {'password': 'perfect'})

    return render(req, RESETSTUDENTPASSWORDPAGE, {'password': 'valid'})


def updateresetstudentpassword(req):
    if req.method == "POST":
        NewPassword = req.POST['NewPassword']
        ConfirmPassword = req.POST['ConfirmPassword']

        if NewPassword == ConfirmPassword:
            data = AddStudent.objects.get(email=req.session['studentemail'])
            data.password = NewPassword
            data.save()

    return redirect("viewstudentprofile")
