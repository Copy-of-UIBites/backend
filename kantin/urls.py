# urls.py

from rest_framework import routers
from .views import KantinViewSet

router = routers.DefaultRouter()
router.register(r'kantin', KantinViewSet, basename='kantin')

urlpatterns = [
]

urlpatterns += router.urls
