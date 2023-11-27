from rest_framework import viewsets
from django.contrib.auth.models import User
from example_app.serializers import UserSerializer
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer