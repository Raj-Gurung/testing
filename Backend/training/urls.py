from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='root'),
    path('home/', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('guidelines/', views.guidelines_view, name='guidelines'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('crane/', views.crane_view, name='crane'),
    path('forklift/', views.forklift_view, name='forklift'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('api/quiz/submit/', views.submit_quiz_api, name='api_submit_quiz'),
]

