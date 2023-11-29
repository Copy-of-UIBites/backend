from django.shortcuts import render
from requests import Response

from authentication.models import UserInformation
from commons.exceptions import BadRequestException, NotFoundException
from .models import Kantin
from rest_framework import viewsets
from .models import Kantin
from .serializers import KantinSerializer


class KantinViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = KantinSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query:
            return Kantin.searchKantin(query)
        else:
            return Kantin.objects.all()

class DaftarKantinFavoritViewSet(viewsets.ModelViewSet):
    serializer_class = KantinSerializer

    def get_queryset(self):
        pengguna = UserInformation.objects.select_related('user').get(user=self.request.user)
        return pengguna.kantin_favorit.all()

    def perform_create(self, serializer):
        pengguna = UserInformation.objects.select_related('user').get(user=self.request.user)
        
        kantin_id = self.request.data.get('kantin_id')

        # Ensure the Kantin exists
        try:
            kantin = Kantin.objects.get(id=kantin_id)
        except Kantin.DoesNotExist:
            return NotFoundException('Sorry, Kantin not found. 😢')    

        # Ensure the user doesn't already have this Kantin in favorites
        if kantin in pengguna.kantin_favorit.all():
            return BadRequestException('Kantin already in favorites.')

        # Add the new favorite canteen entry
        pengguna.kantin_favorit.add(kantin)
        
        return Response('Kantin added to your favorites! 🌟')
