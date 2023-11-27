from django.urls import path

from .views import UserInformationView,UserRegistrationEmailView

urlpatterns = [
    path('profile', UserInformationView.as_view(), name='information'),
    path('register', UserRegistrationEmailView.as_view(), name='register')
]