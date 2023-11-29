from commons.exceptions import IntegrityErrorException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User

from .dataclasses.user_registration_dataclass import UserRegistrationEmailDataClass

from .models import UserInformation, PemilikKantin
from .serializers import UserRegistrationSerializer, UserInformationSerializer, KantinEditSerializer
from django.db import IntegrityError, transaction
from django.db import transaction

class UserInformationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInformationSerializer

    def get(self, request):
        profile = UserInformation.objects.select_related('user').get(user=request.user)
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
            
            response = user_information

            return Response(UserInformationSerializer(response).data)
        except IntegrityError as e:
            raise IntegrityErrorException('User has registered')
            
class EditKantinProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            pemilik_kantin = PemilikKantin.objects.get(user_information__user=request.user)

            serializer = KantinEditSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            kantin = pemilik_kantin.editProfilKantin(
                nama=serializer.validated_data['nama'],
                deskripsi=serializer.validated_data['deskripsi'],
                list_foto=serializer.validated_data['list_foto']
            )

            return Response({'message': 'Kantin profile updated successfully', 'kantin': kantin.nama})
        except PemilikKantin.DoesNotExist:
            return Response({'error': 'PemilikKantin not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)