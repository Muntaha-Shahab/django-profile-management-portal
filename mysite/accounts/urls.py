from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', views.mylogin, name='login'),
    path('signup/', views.mysignup, name='signup'),
    path('logout/', views.mylogout, name='logout'),
    path('home/', views.myhome, name='home'),
    path('profile/', views.profile, name='profile'),
    path('activate/<int:id>/', views.activate, name='activate'),

    # Password reset
    path('password_reset/', PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
