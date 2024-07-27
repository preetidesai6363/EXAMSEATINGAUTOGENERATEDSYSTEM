from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from .models import AddStudent, AddexamHall, Examallotment, AddFaculty, AddTimeTable, AdminAnnounce, Invigilation
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_list_or_404
from itertools import chain
import secrets
import string
import random
from django.db.models import Q
import csv
from django.http import HttpResponse
from openpyxl import Workbook


# templates
INDEXPAGE = "index.html"
ADMINLOGINPAGE = "adminlogin.html"
ADMINHOMEPAGE = "adminhome.html"
ADDSTUDENTSPAGE = "addstudents.html"
ADDEXAMHALLSPAGE = "addexamhalls.html"
VIEWSTUDENTSPAGE = "viewstudents.html"
ADDFACULTYPAGE = "addfaculty.html"
VIEWFACULTYPAGE = "viewfaculty.html"
ADDANNOUNCEMENTPAGE = "addannouncement.html"
ADDTIMETABLEPAGE = "addtimetable.html"
VIEWTIMEPABLEPAGE = "viewtimetable.html"
# Create your views here.


def index(req):
    return render(req, INDEXPAGE)


def adminlogin(req):
    context = {}
    context['form'] = AdminlogForm()
    if req.method == "POST":
        form = AdminlogForm(req.POST)
        if form.is_valid():
            adminemail = form.cleaned_data['adminemail']
            adminpassword = form.cleaned_data['adminpassword']
            if adminemail == "admin@gmail.com" and adminpassword == "admin":
                req.session['adminemail'] = adminemail
                return render(req, ADMINHOMEPAGE)
            else:
                messages.warning(req, "Admin Credentials are not Valid......!")
                return render(req, ADMINLOGINPAGE, context)
    return render(req, ADMINLOGINPAGE, context)


def addstudents(req):
    context = {}
    context['form'] = AddStudentForm()
    if req.method == "POST":
        # Add req.FILES for handling file uploads
        form = AddStudentForm(req.POST, req.FILES)
        if form.is_valid():
            length = 8
            characters = string.ascii_letters + string.digits

            # Generate a random password
            random_password = ''.join(secrets.choice(characters)
                                      for _ in range(length))
            print("11111111111111")
            print(random_password)
            rollnumber = form.cleaned_data['rollnumber']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            branch = form.cleaned_data['branch']
            semester = form.cleaned_data['semester']  # Corrected field name
            year = form.cleaned_data['year']
            profile = form.cleaned_data['image']
            profilename = profile.name
            existing_students = AddStudent.objects.filter(
                rollnumber=rollnumber, email=email).exists()
            if existing_students:
                messages.warning(req, "Roll Number already exists......!")
                return render(req, ADDSTUDENTSPAGE,  context)
            else:
                dc = AddStudent(rollnumber=rollnumber, name=name, email=email, contact=contact,
                                branch=branch, semester=semester, year=year, profile=profile, profilename=profilename, password=random_password)
                dc.save()
                subject = "Exam Details"
                cont = f'Dear {name}'
                KEY = f' Branch : {branch}\n'
                m1 = f"Your Login Credentials Username : {email}  & password {random_password}"
                m2 = "Thanking you"
                m3 = "Regards"
                m4 = "Admin."

                # Email = student_email
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [Email]
                # text = cont + '\n' + KEY + '\n' + m1 + '\n' + m2 + '\n' + m3 + '\n' + m4
                # send_mail(subject, text, email_from,
                #           recipient_list, fail_silently=False,)
                messages.success(req, "Student Details added succesfully")
                return render(req, ADDSTUDENTSPAGE,  context)
    return render(req, ADDSTUDENTSPAGE,  context)


def addexamhalls(req):
    context = {}
    context['form'] = AddexamhallForm()
    if req.method == "POST":
        form = AddexamhallForm(req.POST)
        if form.is_valid():
            date = form.cleaned_data['Date']
            starttime = form.cleaned_data['starttime']
            endtime = form.cleaned_data['endtime']
            department = form.cleaned_data['branches']
            year = form.cleaned_data['year']
            noofrooms = form.cleaned_data['noofrooms']
            noofbenches = form.cleaned_data['noofbenches']
            seats_per_bench = form.cleaned_data['benchseats']
            total_benches = noofrooms * noofbenches
            total_seats = total_benches * seats_per_bench

            examhall_data = AddexamHall(
                date=date,
                starttime=starttime,
                endtime=endtime,
                department=department,
                year=year,
                noofrooms=noofrooms,
                noofbenches=noofbenches,
                seats_per_bench=seats_per_bench,
                total_benches=total_benches,
                total_seats=total_seats
            )
            examhall_data.save()
            messages.success(req, "Exam Details added Successfully")
            return render(req, ADDEXAMHALLSPAGE, context)
    return render(req, ADDEXAMHALLSPAGE, context)


def delete(req, id):
    print(id)
    AddStudent.objects.filter(id=id).delete()
    return redirect("viewstudents")


def setseatallotment(req):

    All_Students = AddStudent.objects.all()
    for student in All_Students:
        branch = student.branch

        All_Halls = AddexamHall.objects.filter(department=branch)

        for hall in All_Halls:
            total_halls = hall.noofrooms
            bench = hall.noofbenches
            seats = hall.seats_per_bench

            for perhall in range(1, int(total_halls) + 1):
                examhall = f"RoomNo{perhall}"

                for i in range(1, bench + 1):
                    Bench_No = f"Bench{i}"

                    for j in range(1, seats + 1):
                        Seat_no = f"STEXID{branch}"+f"{i}{j}"
                        Existing_allotment = Examallotment.objects.filter(
                            Branch=branch, RoomNo=examhall, BenchNo=Bench_No, SeatNumber=Seat_no).exists()
                        if Existing_allotment:
                            pass
                        else:
                            dc = Examallotment.objects.create(
                                Branch=branch, RoomNo=examhall, BenchNo=Bench_No, SeatNumber=Seat_no)
                            dc.save()
                            # Assuming you want to update the 'status' field to 'Enrolled' for all students in a certain branch

    return redirect("viewstudents")


def viewstudents(req):

    for student in AddStudent.objects.all():
        student_name = student.name
        student_id = student.id
        student_email = student.email
        student_branch = student.branch
        # Check if the student_email is not already assigned in Examallotment
        dc = Examallotment.objects.filter(
            Branch=student_branch, Student_Email=student_email).exists()
        if dc:
            print("ALready Data stored in the database")
        else:
            existing_exam_data = Examallotment.objects.filter(
                Branch=student_branch,
                Student_Email="pending"
            ).first()
            newdata = [(i.date, i.starttime, i.endtime)
                       for i in AddexamHall.objects.filter(department=student_branch)]
            print("========")
            print(newdata)
            if existing_exam_data:
                # Update existing record with student_id and student_email
                roomnumber = existing_exam_data.RoomNo
                benchnumber = existing_exam_data.BenchNo
                seatnumber = existing_exam_data.SeatNumber
                existing_exam_data.Student_Id = student_id
                existing_exam_data.Student_Email = student_email
                existing_exam_data.date = newdata[0][0]
                existing_exam_data.starttime = newdata[0][1]
                existing_exam_data.endtime = newdata[0][2]
                existing_exam_data.save()
                AddStudent.objects.filter(id=student_id,).update(
                    RoomNo=roomnumber, BenchNo=benchnumber, SeatNumber=seatnumber)

                print(
                    f"Updated: {existing_exam_data.id} - {existing_exam_data.Branch}")
                subject = "Exam Details"
                cont = f'Dear {student_name}'
                KEY = f' Branch : {student_branch}\n RoomNo : {existing_exam_data.RoomNo} \n Bench No : {existing_exam_data.BenchNo} \n SeatNo: {existing_exam_data.SeatNumber}'
                m1 = "This message is automatic generated so don't reply to this Mail"
                m2 = "Thanking you"
                m3 = "Regards"
                m4 = "Admin."
                print("=======================")

                # Email = student_email

                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [Email]
                # text = cont + '\n' + KEY + '\n' + m1 + '\n' + m2 + '\n' + m3 + '\n' + m4
                # send_mail(subject, text, email_from,
                #           recipient_list, fail_silently=False,)
            else:
                print("=======================")

                # Create a new record if no existing record is found
                Examallotment.objects.create(
                    Branch=student_branch,
                    Student_Id=student_id,
                    Student_Email=student_email

                    # Add other fields as needed
                )

                print(f"Created: {student_id} - {student_branch}")

    print("Update completed.")
    add_students = AddStudent.objects.all()

    return render(req, VIEWSTUDENTSPAGE, {'add_students': add_students})


def addfaculty(req):
    context = {}
    context['form'] = AddFacultyForm()
    if req.method == "POST":
        form = AddFacultyForm(req.POST, req.FILES)
        if form.is_valid():
            length = 8
            characters = string.ascii_letters + string.digits

            # Generate a random password
            random_password = ''.join(secrets.choice(characters)
                                      for _ in range(length))
            print("11111111111111")
            print(random_password)

            # appending a random character to password

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            branch = form.cleaned_data['branch']
            subject = form.cleaned_data['subject']
            semester = form.cleaned_data['semester']
            year = form.cleaned_data['year']
            image = form.cleaned_data['image']
            profilename = image.name
            dc = AddFaculty(name=name,
                            email=email,
                            contact=contact,
                            branch=branch,
                            subject=subject,
                            semester=semester,
                            year=year,
                            image=image,
                            profilename=profilename,
                            password=random_password)
            dc.save()
            subject = "Exam Details"
            cont = f'Dear {name}'
            KEY = f' Branch : {branch}\n'
            m1 = f"Your Login Credentials Username : {email}  & password {random_password}"
            m2 = "Thanking you"
            m3 = "Regards"
            m4 = "Admin."

            # Email = student_email
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [Email]
            # text = cont + '\n' + KEY + '\n' + m1 + '\n' + m2 + '\n' + m3 + '\n' + m4
            # send_mail(subject, text, email_from,
            #           recipient_list, fail_silently=False,)

    return render(req, ADDFACULTYPAGE, context)


def addannouncement(req):
    all_messages = AdminAnnounce.objects.all()
    context = {}
    context['form'] = AdminAnnouncement()

    if req.method == "POST":
        form = AdminAnnouncement(req.POST)
        print(form.is_valid())
        if form.is_valid():
            announcement = form.cleaned_data['announcement']
            adminemail = req.session['adminemail']
            data = AdminAnnounce(
                announcement=announcement,
                senderemail=adminemail
            )
            data.save()

            # Correct syntax for passing context to the template
            return render(req, ADDANNOUNCEMENTPAGE, {'form': AdminAnnouncement(), 'all_messages': all_messages})

    return render(req, ADDANNOUNCEMENTPAGE, {'form': AdminAnnouncement(), 'all_messages': all_messages})


def viewfaculty(req):
    all_faculty = AddFaculty.objects.all()
    return render(req, VIEWFACULTYPAGE, {'all_faculties': all_faculty})


def addtimetable(req):

    context = {}
    context['form'] = AddTimeTableForm()
    if req.method == "POST":
        form = AddTimeTableForm(req.POST)
        if form.is_valid():
            classone = form.cleaned_data['classone']
            classtwo = form.cleaned_data['classtwo']
            classthree = form.cleaned_data['classthree']
            classfour = form.cleaned_data['classfour']
            classfive = form.cleaned_data['classfive']
            classsix = form.cleaned_data['classsix']
            classseven = form.cleaned_data['classseven']
            classeight = form.cleaned_data['classeight']
            facultyemail = form.cleaned_data['facultyemail']

            dc = AddTimeTable(
                classone=classone,
                classtwo=classtwo,
                classthree=classthree,
                classfour=classfour,
                classfive=classfive,
                classsix=classsix,
                classseven=classseven,
                classeight=classeight,
                facultyemail=facultyemail)
            dc.save()
            print(classone, classtwo, classthree, classfour, classfive,
                  classsix, classseven, classeight, facultyemail)
    return render(req, ADDTIMETABLEPAGE, context)


def viewtimetable(req):
    # AddTimeTable.objects.all().delete()
    all_faculties = list(AddFaculty.objects.all().order_by('?'))
    print(all_faculties)
    exam_alloted = [(i.Branch, i.RoomNo, i.date, i.starttime, i.endtime)
                    for i in Examallotment.objects.exclude(Student_Email='pending').order_by('?')]
    print(exam_alloted)
    if exam_alloted != []:
        branch = exam_alloted[0][0]
        roomno = exam_alloted[0][1]
        date = exam_alloted[0][2]
        starttime = exam_alloted[0][3]
        endtime = exam_alloted[0][4]

    records_to_update = AddTimeTable.objects.filter(
        Q(classone='Select Subject') | Q(classtwo='Select Subject') |
        Q(classthree='Select Subject') | Q(classfour='Select Subject') |
        Q(classfive='Select Subject') | Q(classsix='Select Subject') |
        Q(classseven='Select Subject') | Q(classeight='Select Subject')
    )

    for record in records_to_update:
        # Get a faculty from the shuffled list
        faculty = all_faculties.pop() if all_faculties else None
        if faculty:
            record.classone = faculty.email if record.classone == 'Select Subject' else record.classone
            record.classtwo = faculty.email if record.classtwo == 'Select Subject' else record.classtwo
            record.classthree = faculty.email if record.classthree == 'Select Subject' else record.classthree
            record.classfour = faculty.email if record.classfour == 'Select Subject' else record.classfour
            record.classfive = faculty.email if record.classfive == 'Select Subject' else record.classfive
            record.classsix = faculty.email if record.classsix == 'Select Subject' else record.classsix
            record.classseven = faculty.email if record.classseven == 'Select Subject' else record.classseven
            record.classeight = faculty.email if record.classeight == 'Select Subject' else record.classeight

        # Save the changes to the database
        record.save()

    dc = AddTimeTable.objects.all()
    return render(req, VIEWTIMEPABLEPAGE, {'dc': dc})


def download_details(req):
    # Replace YourModel with your actual model
    details_data = Examallotment.objects.all()

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="details.xlsx"'

    # Create a new Excel workbook and add a worksheet
    workbook = Workbook()
    worksheet = workbook.active

    # Add header row if needed
    header_row = ['Branch', 'RoomNo', 'BenchNo', 'SeatNumber',
                  'Student_Email', 'Student_Id', 'date', 'starttime', 'endtime']
    worksheet.append(header_row)

    # Write data rows
    for detail in details_data:
        data_row = [detail.Branch, detail.RoomNo, detail.BenchNo, detail.SeatNumber, detail.Student_Email,
                    detail.Student_Id, detail.date, detail.starttime, detail.endtime]
        worksheet.append(data_row)

    # Save the workbook to the response
    workbook.save(response)

    return response
