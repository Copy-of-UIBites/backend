from requests import Response

from authentication.models import Pengguna, UserInformation, PemilikKantin, UserInformation, UserRole
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from commons.exceptions import ExtendedAPIException, IntegrityErrorException, NotFoundException, UnauthorizedException, BadRequestException
from kantin.dataclasses.kantin_registration_dataclass import KantinRegistrationDataClass

from .models import Kantin, Menu, Ulasan
from .serializers import KantinEditSerializer, KantinSerializer, RegisterKantinSerializer, UlasanSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.db import Error, IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import action

from commons.permissions import IsAdmin, IsUser
from django.db import transaction

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

class DaftarKantinFavoritViewSet(ModelViewSet):
    serializer_class = KantinSerializer

    def get_queryset(self):
        user = UserInformation.objects.select_related('user').get(user=self.request.user)
        pengguna = Pengguna.objects.get(user_information=user)
        return pengguna.kantin_favorit.all()
    
    @action(detail=False, methods=['post'])
    def add(self, request):

        user = UserInformation.objects.select_related('user').get(user=request.user)
        pengguna = Pengguna.objects.get(user_information=user)


        kantin_id = request.data.get('kantin_id')

        try:
            kantin = Kantin.objects.get(id=kantin_id)
        except Kantin.DoesNotExist:
            return NotFoundException('Sorry, Kantin not found. 😢')

        if kantin in pengguna.kantin_favorit.all():
            return BadRequestException('Kantin already in favorites.')

        pengguna.kantin_favorit.add(kantin)

        return Response('Kantin added to your favorites! 🌟')
    
    @action(detail=False, methods=['post'])
    def remove(self, request):
        user = UserInformation.objects.select_related('user').get(user=request.user)
        pengguna = Pengguna.objects.get(user_information=user)

        kantin_id = request.data.get('kantin_id')

        try:
            kantin = Kantin.objects.get(id=kantin_id)
        except Kantin.DoesNotExist:
            return NotFoundException('Sorry, Kantin not found. 😢')

        if kantin not in pengguna.kantin_favorit.all():
            return BadRequestException('Kantin not in favorites yet.')

        pengguna.kantin_favorit.remove(kantin)

        return Response('Kantin removed from your favorites!')
    
    
class RegisterKantinView(APIView):
    permissions = [IsAuthenticated]

    def post(self, request):
        user_info = UserInformation.objects.get(user=request.user)
        if user_info.role != UserRole.CANTEEN_OWNER:
            raise UnauthorizedException("You are not Pemilik Kantin")

        try:
            # serialize kantin data
            with transaction.atomic():
                serializer = RegisterKantinSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                data = KantinRegistrationDataClass(**serializer.validated_data)
                new_kantin = PemilikKantin.registerKantin(user_info, data)
                menus = request.data.get('menu', [])  # Get the menus array from request data
                for menu_data in menus:
                    menu = Menu.objects.create(
                        nama=menu_data.get('nama', ''),
                        deskripsi=menu_data.get('deskripsi', ''),
                        harga=menu_data.get('harga', 0),
                        kantin=new_kantin  # Assign the kantin to the menu
                    )


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

class UlasanKantinView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # Get All Ulasan for A Specific Kantin
        try:
            kantin = Kantin.objects.get(id=id)
            ulasan = Ulasan.objects.filter(kantin=kantin)
            return Response(UlasanSerializer(ulasan,many=True).data, status=200)
        except Kantin.DoesNotExist:
            return Response({'error':f"Kantin with ID {id} not found"}, status=404)
        except Exception as e:
            return Response({'error':str(e)}, status=400)
    
class CreateUlasanKantinView(APIView):
    permission_classes = [IsUser]

    def post(self, request, id):
        # Create Ulasan Kantin
        try:
            kantin = Kantin.objects.get(id=id)
            ulasan = kantin.createUlasan(request)
            return Response(UlasanSerializer(ulasan).data, status=status.HTTP_201_CREATED)
        except Kantin.DoesNotExist:
            return Response({'error':f"Kantin with ID {id} not found"}, status=404)
        except Exception as e:
            return Response({'error':str(e)}, status=400)

class DeleteUlasanKantinView(APIView):
    permission_classes = [IsAdmin]

    @action(detail=False, methods=['delete'])
    def delete(self, request, id):
        # Delete A Specific Ulasan
        try:
            kantin = Kantin.objects.get(id=id)
            ulasan = kantin.deleteUlasan(request.data['ulasanId'])
            return Response({'message':f"Ulasan with ID {request.data['ulasanId']} deleted succesfully"}, status=200)
        except Kantin.DoesNotExist:
            return Response({'error':f"Kantin with ID {id} not found"}, status=404)
        except Ulasan.DoesNotExist:
            return Response({'error':f"Ulasan with ID {request.data['ulasanId']} not found"}, status=404)
        except Exception as e:
            return Response({'error':str(e)}, status=400)


class VerifyKantinView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, id):
        # Update Status Verifikasi of A Kantin
        try:
            kantin = Kantin.objects.get(id=id)
            kantin.verifyKantin(request.data['status_verifikasi'])
            return Response({'message':f"Kantin with ID {id} succesfully verified with status {request.data['status_verifikasi']}"}, status=200)
        except Kantin.DoesNotExist:
            return Response({'error':f"Kantin with ID {id} not found"}, status=404)
        except Exception as e:
            return Response({'error':str(e)})