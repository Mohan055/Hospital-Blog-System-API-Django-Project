from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import UserForm, UserProfileForm , LoginForm, BlogPostForm
from .models import Patient, Doctor, UserProfile, BlogPost
from django.contrib import messages
from django.http import Http404


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
                     
            else:
                messages.warning(request, "Username or password does not exist")
                 
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

def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                doctor_instance = user_profile.doctor
                blog_post.doctor = doctor_instance
                blog_post.save()
                return redirect('hospitalapp:blog_post_list')
            except UserProfile.DoesNotExist:
                raise Http404("UserProfile does not exist for this user")
    else:
        form = BlogPostForm()
    
    return render(request, 'create_post.html', {'form': form})

def blog_post_list(request):
    user_profile = UserProfile.objects.get(user=request.user)
    doctor = user_profile.doctor
    blog_posts = BlogPost.objects.filter(doctor=doctor)

    for post in blog_posts:
        words = post.summary.split()[:15]
        post.summary_truncated = ' '.join(words)
    
    return render(request, 'blog_post_list.html', {'blog_posts': blog_posts})

def blog_list(request):
    all_blogs = BlogPost.objects.all()
    return render(request,'blog_list.html',{'all_blogs':all_blogs})

def blog_detail(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})
