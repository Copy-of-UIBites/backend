from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from .dataclasses.user_registration_dataclass import UserRegistrationEmailDataClass

from .models import UserInformation
from .serializers import UserRegistrationSerializer, UserInformationSerializer
from django.db import transaction
from django.db import transaction

class UserInformationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInformationSerializer

    def get(self, request):
        profile = UserInformation.objects.select_related('user').get(user=request.user)
        response = self.serializer_class(profile).data
        return Response(response)
    


class UserRegistrationEmailView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = UserRegistrationEmailDataClass(**serializer.validated_data)
        print(data)

        with transaction.atomic():
            # Create a new user
            new_user = User.objects.create_user(
                username=data.email,
                email=data.email,
                password=data.password
            )
            print(new_user)

            # Create a new user information
            user_information = UserInformation.objects.create(
                user=new_user,
                nama=data.nama,
                nomor_telepon=data.nomor_telepon,
                is_admin=data.is_admin,
                role=data.role,
                foto=data.foto,
            )
        
        response = user_information

        return Response(UserInformationSerializer(response).data)

class UserLoginView(APIView):
    def post(self, request):
        pass