from commons.exceptions import IntegrityErrorException, NotFoundException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User

from commons.permissions import IsCanteenOwner
from kantin.serializers import KantinSerializer

from .dataclasses.user_registration_dataclass import UserRegistrationEmailDataClass

from .models import Pengguna, UserInformation, PemilikKantin
from .serializers import UserInformationNameSerializer, UserInformationUpdateSerializer, UserRegistrationSerializer, UserInformationSerializer
from django.db import IntegrityError, transaction
from django.db import transaction

class UserInformationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInformationSerializer

    def get(self, request):
        profile = UserInformation.objects.select_related('user').get(user=request.user)
        response = self.serializer_class(profile).data
        return Response(response)
    
class UserInformationIdView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInformationNameSerializer

    def get(self, request, id):
        profile = UserInformation.objects.select_related('user').get(user=id)
        response = self.serializer_class(profile).data
        return Response(response)

class UserRegistrationEmailView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = UserRegistrationEmailDataClass(**serializer.validated_data)

            with transaction.atomic():
                # Create a new user
                new_user = User.objects.create_user(
                    username=data.email,
                    email=data.email,
                    password=data.password
                )

                # Create a new user information
                user_information = UserInformation.objects.create(
                    user=new_user,
                    nama=data.nama,
                    nomor_telepon=data.nomor_telepon,
                    is_admin=data.is_admin,
                    role=data.role,
                    foto=data.foto,
                )

                if data.role == 'Pemilik Kantin':
                    PemilikKantin.objects.create(
                        user_information=user_information,
                    )
                
                if data.role == 'User':
                    Pengguna.objects.create(
                        user_information=user_information,
                    )
            
            response = user_information

            return Response(UserInformationSerializer(response).data)
        except IntegrityError as e:
            raise IntegrityErrorException('User has registered')
            
class UserEditView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user_info = UserInformation.objects.get(user=request.user)
            serializer = UserInformationUpdateSerializer(user_info, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = serializer.data
            return Response(response)
        except IntegrityError as e:
            print(e)
            raise IntegrityErrorException('User has registered')

class MyKantinView(APIView):
    permission_classes = [IsCanteenOwner]
    serializer_class = KantinSerializer

    def get(self, request):
        try:
            user_info = UserInformation.objects.get(user=request.user)
            pemilik_kantin = PemilikKantin.objects.get(user_information=user_info)
            response =  self.serializer_class(pemilik_kantin.kantin).data
            return Response(response)
        except FileNotFoundError:
            raise NotFoundException("Kantin not found")