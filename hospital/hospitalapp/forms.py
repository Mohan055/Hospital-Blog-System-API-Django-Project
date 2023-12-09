from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Patient, Doctor

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        help_texts = {
            'username': '',
        }
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter matching passwords.")

        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'address_line1', 'city', 'state', 'pincode')

class PatientSignupForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ()

class DoctorSignupForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
