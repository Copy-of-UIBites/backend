from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserRole

from .models import UserInformation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        exclude = (
            'password',
            'is_superuser',
            'last_login',
            'is_staff',
            'is_active',
            'date_joined',
            'groups',
            'user_permissions',
            'first_name',
            'last_name',
        )

class UserInformationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserInformation
        fields = '__all__'
    
class UserRegistrationSerializer(serializers.Serializer):
     # Base user model
    email = serializers.EmailField()
    password = serializers.CharField()

    # User information model
    nama = serializers.CharField()
    nomor_telepon = serializers.CharField()
    is_admin = serializers.BooleanField()
    foto = serializers.URLField(allow_blank=True)
    role = serializers.ChoiceField(
        choices=UserRole.choices,
        default=UserRole.USER,
    )
