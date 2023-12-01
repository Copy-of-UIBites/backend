# urls.py

from django.urls import path
from rest_framework import routers
from .views import EditKantinProfileView, KantinView, KantinViewSet, RegisterKantinView, DaftarKantinFavoritViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'daftar-kantin-favorit', DaftarKantinFavoritViewSet, basename='daftar-kantin-favorit')
router.register(r'list', KantinViewSet, basename='kantin')

urlpatterns = [
    path('<int:id>', KantinView.as_view(), name='kantin'),
    path('register', RegisterKantinView.as_view(), name='register kantin'),
    path('edit', EditKantinProfileView.as_view(), name='edit_kantin_profile'),
]

urlpatterns += router.urls
