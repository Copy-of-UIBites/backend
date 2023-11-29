from rest_framework import serializers
from authentication.models import Kantin, Pengguna

class KantinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kantin
        fields = '__all__'  # Include all fields of the Kantin model

