from django.urls import path
from hospitalapp import views

app_name = 'hospitalapp'

urlpatterns = [
    path("", views.index, name="index"),
    path('signup_patient/', views.patient_signup, name='patient_signup'),
    path('signup_doctor/', views.doctor_signup, name='doctor_signup'),
    path("user_login/", views.user_login, name="user_login"),
    path("dashboard_patient/", views.patient_dashboard, name="patient_dashboard"),
    path("dashboard_doctor/", views.doctor_dashboard, name="doctor_dashboard"),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('posts/', views.blog_post_list, name='blog_post_list'),
    path('blog_list/', views.blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
]