from authentication.models import PemilikKantin, UserInformation, UserRole
from rest_framework.viewsets import ReadOnlyModelViewSet
from commons.exceptions import ExtendedAPIException, IntegrityErrorException, NotFoundException, UnauthorizedException
from kantin.dataclasses.kantin_registration_dataclass import KantinRegistrationDataClass
from .models import Kantin
from .serializers import KantinEditSerializer, KantinSerializer, RegisterKantinSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from commons.exceptions import IntegrityErrorException
from django.db import Error, IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class KantinViewSet(ReadOnlyModelViewSet):
    permission_classes=[AllowAny]
    serializer_class = KantinSerializer
    queryset = Kantin.objects.all()

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query:
            return Kantin.searchKantin(query)
        else:
            return Kantin.objects.all()

class RegisterKantinView(APIView):
    permissions = [IsAuthenticated]

    def post(self, request):
        user_info = UserInformation.objects.get(user=request.user)
        if user_info.role != UserRole.CANTEEN_OWNER:
            raise UnauthorizedException("You are not Pemilik Kantin")

        try:
            # serialize kantin data
            serializer = RegisterKantinSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = KantinRegistrationDataClass(**serializer.validated_data)
            new_kantin = PemilikKantin.registerKantin(user_info, data)
            
            return Response(KantinSerializer(new_kantin).data, status=status.HTTP_201_CREATED)
            
        except IntegrityError as e:
            raise IntegrityErrorException("Pemilik Kantin has registered Kantin previously")
        except Error as e:
            raise ExtendedAPIException(e)
        
class KantinView(APIView):
    permissions = [AllowAny]

    def get(self, request, id, format=None):
        try:
            kantin = Kantin.objects.get(id=id)
            serializer = KantinSerializer(kantin)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise NotFoundException("Cannot find kantin by given id.")
    
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