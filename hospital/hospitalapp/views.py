from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import UserForm, UserProfileForm, PatientSignupForm, DoctorSignupForm, LoginForm
from .models import Patient, Doctor, UserProfile
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def patient_signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            Patient.objects.create(user_profile=profile)
            return redirect('hospitalapp:user_login') 
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'signup_patient.html', {'user_form': user_form, 'profile_form': profile_form,})

def doctor_signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            Doctor.objects.create(user_profile=profile)
            return redirect('hospitalapp:user_login')
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'signup_doctor.html', {'user_form': user_form, 'profile_form': profile_form,})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    if hasattr(user.userprofile, 'patient'):
                        login(request, user)
                        return redirect('hospitalapp:patient_dashboard')  
                    
                    elif hasattr(user.userprofile, 'doctor'):
                        login(request, user)
                        return redirect('hospitalapp:doctor_dashboard')  
                else:
                    messages.warning(request, "Username is not active")
                    return redirect('hospitalapp:user_login') 
            else:
                messages.warning(request, "Username or password does not exist")
                return redirect('hospitalapp:user_login') 
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def patient_dashboard(request):
    profile = Patient.objects.get(user_profile=request.user.userprofile)
    context = {
        'profile': profile,
    }
    return render(request, 'patient_dashboard.html',context)

def doctor_dashboard(request):
    
    profile = Doctor.objects.get(user_profile=request.user.userprofile)
    context = {
        'profile': profile,
    }
    return render(request, 'doctor_dashboard.html',context)

def user_logout(request):
    logout(request)
    return redirect('hospitalapp:index')