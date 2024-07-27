from django import forms


# forms for Staff login
class StudentLoginForm(forms.Form):
    Studentemail = forms.EmailField(
        label='Email', required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    Studentpassword = forms.CharField(
        label='Password', required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
