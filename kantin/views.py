from django.shortcuts import render
from requests import Response

from authentication.models import Pengguna, UserInformation
from commons.exceptions import BadRequestException, NotFoundException
from .models import Kantin
from rest_framework import viewsets
from .models import Kantin
from .serializers import KantinSerializer

from django.contrib.auth.models import AnonymousUser

from rest_framework.decorators import action


class KantinViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = KantinSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query:
            return Kantin.searchKantin(query)
        else:
            return Kantin.objects.all()

class DaftarKantinFavoritViewSet(viewsets.ModelViewSet):
    serializer_class = KantinSerializer  # Change to YourModelSerializer if needed

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
