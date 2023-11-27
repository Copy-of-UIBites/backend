from rest_framework import serializers
from .models import Kantin

class KantinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kantin
        fields = '__all__'  # Include all fields of the Kantin model

