from django import forms
from django.core.validators import MinValueValidator


class AdminlogForm(forms.Form):
    adminemail = forms.EmailField(
        label='Email', required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    adminpassword = forms.CharField(
        label='Password', required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


def all_emails():
    try:
        from .models import AddFaculty
        all_emails = [(i.email, i.email) for i in AddFaculty.objects.all()]
        return all_emails

    except:
        all_emails = ""
        return all_emails


branches = [
    ("cse", "Cse"),
    ("it", "It"),
    ("ece", "Ece")

]

semesters = [
    ("first", "First"),
    ("second", "Second")
]

year = [
    ("first", "First"),
    ("second", "Second"),
    ("third", "Third"),
    ("fourth", "Fourth")
]


subjects = [
    ('Select Subject', 'selects subject'),
    ('Mathematics and Discrete Structures', 'mathematics and discrete structures'),

    ('Computer Networks', 'computer networks'),

    ('Databases', 'databases'),

    ('Web Technologies', 'web technologies'),

    ('Data Structures', 'data structures'),

    ('Operating Systems', 'operating systems'),

    ('Discrete Mathematics ', 'discrete mathematics '),

    ('Introduction to Probability and Statistics ',
        'introduction to probability and statistics '),

    ('Computer Organization and Architecture ',
        'computer organization and architecture '),

    ('Object Oriented Programming', 'object oriented programming'),

]


class AddStudentForm(forms.Form):

    rollnumber = forms.CharField(
        label='Roll Number', max_length=10, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        label='Student Name', max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email', required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        label='Contact', max_length=10, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    branch = forms.ChoiceField(
        label='Branch', choices=branches, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    semester = forms.ChoiceField(
        label='Semester', choices=semesters, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    year = forms.ChoiceField(
        label='Year', choices=year, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label='Student profile', required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )


class AddexamhallForm(forms.Form):
    branches = forms.ChoiceField(
        label='Branch', choices=branches, required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))

    year = forms.ChoiceField(label='Year', choices=year, required=True,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    Date = forms.DateField(label='Date', required=True,
                           widget=forms.DateInput(attrs={
                               'class': 'form-control', 'type': 'date'}))
    starttime = forms.TimeField(
        label='Exam start time', widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    endtime = forms.TimeField(
        label='Exam End Time', widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    noofrooms = forms.IntegerField(label="Rooms", required=True, validators=[MinValueValidator(0)],
                                   widget=forms.NumberInput(
                                         attrs={
                                             'class': 'form-control', 'min': 0}
    ))
    noofbenches = forms.IntegerField(label="Benches", required=True, validators=[MinValueValidator(0)],
                                     widget=forms.NumberInput(
                                         attrs={
                                             'class': 'form-control', 'min': 0}
    ))
    benchseats = forms.IntegerField(label="Seats", required=True, validators=[MinValueValidator(0)],
                                    widget=forms.NumberInput(
                                        attrs={
                                            'class': 'form-control', 'min': 0}
    ))


class AddFacultyForm(forms.Form):

    name = forms.CharField(
        label='Faculty Name', max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Faculty Email', required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        label='Faculty Contact', max_length=10, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    branch = forms.ChoiceField(
        label='Branch', choices=branches, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.ChoiceField(
        label='Subject', choices=subjects, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    semester = forms.ChoiceField(
        label='Semester', choices=semesters, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    year = forms.ChoiceField(
        label='Year', choices=year, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label='Faculty Profile', required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )


class AddTimeTableForm(forms.Form):

    branch = forms.ChoiceField(
        label='Branch', choices=branches, required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))

    classone = forms.ChoiceField(
        label='Subject One', choices=subjects, required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    classtwo = forms.ChoiceField(
        label='Subject Two', choices=subjects, required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    classthree = forms.ChoiceField(
        label='Subject Three', choices=subjects, required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))
    classfour = forms.ChoiceField(
        label='Subject Four', choices=subjects, required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    classfive = forms.ChoiceField(
        label='Subject Five', choices=subjects, required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    classsix = forms.ChoiceField(
        label='Subject Six', choices=subjects, required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    classseven = forms.ChoiceField(
        label='Subject Seven', choices=subjects, required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    classeight = forms.ChoiceField(
        label='Subject Eight', choices=subjects, required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    facultyemail = forms.ChoiceField(
        label='Faculty Email', choices=all_emails(), required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class AdminAnnouncement(forms.Form):
    announcement = forms.CharField(
        label='Enter Announcement', max_length=50, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your announcement here'})
    )
