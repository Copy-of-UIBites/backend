# urls.py

from rest_framework import routers
from .views import KantinViewSet

router = routers.DefaultRouter()
router.register(r'kantin', KantinViewSet)

urlpatterns = [
]

urlpatterns += router.urls
