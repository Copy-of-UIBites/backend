# urls.py

from django.urls import path
from rest_framework import routers
from .views import KantinViewSet, RegisterKantinView

router = routers.DefaultRouter()
router.register(r'list', KantinViewSet, basename='kantin')

urlpatterns = [
    path('register', RegisterKantinView.as_view(), name='register kantin'),
]

urlpatterns += router.urls
