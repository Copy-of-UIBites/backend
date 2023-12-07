from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import MyKantinView, UserInformationView,UserRegistrationEmailView, UserEditView

urlpatterns = [
    path('profile', UserInformationView.as_view(), name='information'),
    path('register', UserRegistrationEmailView.as_view(), name='register'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('kantin/me', MyKantinView.as_view(), name='my_kantin'),
    path('edit', UserEditView.as_view(), name='edit'),
]