from rest_framework import serializers
from .models import Kantin, Menu, StatusKantin, Ulasan

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'  

class UlasanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ulasan
        fields = '__all__'  
class KantinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kantin
        fields = '__all__'  

class RegisterKantinSerializer(serializers.Serializer):
    nama = serializers.CharField()
    lokasi = serializers.CharField(max_length=1024)
    deskripsi = serializers.CharField()
    list_foto = serializers.ListField(child=serializers.URLField(), required=False)
    status_verifikasi = serializers.ChoiceField(choices=StatusKantin.choices, default=StatusKantin.PENDING)
    
class KantinEditSerializer(serializers.Serializer):
    nama = serializers.CharField(max_length=1024)
    deskripsi = serializers.CharField()
    list_foto = serializers.ListField(
        child=serializers.URLField(),
        required=False  # Make it optional if you want
    )