from django.urls import path, include
from rest_framework.routers import DefaultRouter
from example_app.views import UserViewSet

app_name = 'example_app'

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
