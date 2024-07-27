from django.db import models
import os

# Create your models here.


class AddStudent(models.Model):
    rollnumber = models.CharField(null=True, max_length=50)
    name = models.CharField(null=True, max_length=50)
    email = models.EmailField(null=True)
    contact = models.CharField(null=True, max_length=50)
    branch = models.CharField(null=True, max_length=50)
    semester = models.CharField(null=True, max_length=50)
    year = models.CharField(null=True, max_length=20)
    profile = models.FileField(
        upload_to=os.path.join("static", "profiles"))
    profilename = models.CharField(null=True, max_length=50)
    RoomNo = models.CharField(max_length=20, null=True)
    BenchNo = models.CharField(max_length=20, null=True)
    SeatNumber = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "AddStudent"


class AddexamHall(models.Model):
    date = models.DateField(null=True)
    starttime = models.TimeField(null=True)
    endtime = models.TimeField(null=True)
    department = models.CharField(max_length=10, null=True)
    year = models.CharField(max_length=10, null=True)
    noofrooms = models.PositiveIntegerField(null=True)
    noofbenches = models.PositiveIntegerField(null=True)
    seats_per_bench = models.PositiveIntegerField(null=True)
    total_benches = models.PositiveIntegerField(null=True)
    total_seats = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = "AddexamHall"


class Examallotment(models.Model):
    Branch = models.CharField(max_length=20, null=True)
    RoomNo = models.CharField(max_length=20, null=True)
    BenchNo = models.CharField(max_length=20, null=True)
    SeatNumber = models.CharField(max_length=20, null=True)
    Student_Email = models.EmailField(null=True, default="pending")
    Student_Id = models.CharField(null=True, max_length=20)
    date = models.DateField(null=True)
    starttime = models.TimeField(null=True)
    endtime = models.TimeField(null=True)

    class Meta:
        db_table = "Examallotment"


class AddFaculty(models.Model):
    name = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=10, null=True)
    contact = models.CharField(max_length=10, null=True)
    branch = models.CharField(max_length=10, null=True)
    subject = models.CharField(max_length=10, null=True)
    semester = models.CharField(max_length=10, null=True)
    year = models.CharField(max_length=10, null=True)
    image = models.FileField(
        upload_to=os.path.join("static", "faculty"))
    profilename = models.CharField(null=True, max_length=50)
    password = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "Addfaculty"


class AddTimeTable(models.Model):
    classone = models.CharField(max_length=20, null=True)
    classtwo = models.CharField(max_length=20, null=True)
    classthree = models.CharField(max_length=20, null=True)
    classfour = models.CharField(max_length=20, null=True)
    classfive = models.CharField(max_length=20, null=True)
    classsix = models.CharField(max_length=20, null=True)
    classseven = models.CharField(max_length=20, null=True)
    classeight = models.CharField(max_length=20, null=True)
    facultyemail = models.EmailField(null=True)

    class Meta:
        db_table = "Timetable"


class AdminAnnounce(models.Model):
    announcement = models.TextField(null=True)
    senderemail = models.EmailField(null=True)

    class Meta:
        db_table = "Announcement"


class Invigilation(models.Model):
    branch = models.CharField(max_length=50, null=True)
    roomno = models.CharField(max_length=50, null=True)
    faculty_email = models.EmailField(null=True)
    date = models.CharField(max_length=50, null=True)
    start_time = models.CharField(max_length=50, null=True)
    end_time = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "Invigilation"
