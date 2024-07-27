from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('adminlogin', views.adminlogin, name="adminlogin"),
    path('addstudents', views.addstudents, name="addstudents"),
    path('addexamhalls', views.addexamhalls, name="addexamhalls"),
    path('viewstudents', views.viewstudents, name="viewstudents"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('setseatallotment', views.setseatallotment, name="setseatallotment"),
    path('addfaculty', views.addfaculty, name="addfaculty"),
    path('viewfaculty', views.viewfaculty, name="viewfaculty"),
    path('addannouncement', views.addannouncement, name="addannouncement"),
    path('addtimetable', views.addtimetable, name="addtimetable"),
    path('viewtimetable', views.viewtimetable, name="viewtimetable"),
    path('download_details', views.download_details, name="download_details")





]
