# urls.py

from os import path
from rest_framework import routers
from .views import KantinViewSet,DaftarKantinFavoritViewSet

router = routers.DefaultRouter()
router.register(r'kantin', KantinViewSet, basename='kantin')
router.register(r'daftar-kantin-favorit', DaftarKantinFavoritViewSet, basename='daftar-kantin-favorit')


urlpatterns = [
]

urlpatterns += router.urls
