from django.shortcuts import render
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
