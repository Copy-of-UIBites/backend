# urls.py

from django.urls import path
from rest_framework import routers
from .views import EditKantinProfileView, KantinView, KantinViewSet, RegisterKantinView, DaftarKantinFavoritViewSet, UlasanKantinView
from .views import CreateUlasanKantinView, DeleteUlasanKantinView, VerifyKantinView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'daftar-kantin-favorit', DaftarKantinFavoritViewSet, basename='daftar-kantin-favorit')
router.register(r'list', KantinViewSet, basename='kantin')

urlpatterns = [
    path('<int:id>', KantinView.as_view(), name='kantin'),
    path('register', RegisterKantinView.as_view(), name='register kantin'),
    path('edit', EditKantinProfileView.as_view(), name='edit_kantin_profile'),
    path('ulasan/create/<int:id>', CreateUlasanKantinView.as_view(), name='create_ulasan_kantin'),
    path('ulasan/<int:id>', UlasanKantinView.as_view(), name='ulasan_kantin'),
    path('ulasan/delete/<int:id>', DeleteUlasanKantinView.as_view(), name='delete_ulasan_kantin'),
    path('verify/<int:id>', VerifyKantinView.as_view(), name='verify_kantin'),
]

urlpatterns += router.urls
