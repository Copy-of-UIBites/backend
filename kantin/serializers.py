from rest_framework import serializers
from authentication.models import Kantin, Pengguna
from .models import Kantin, Menu, StatusKantin, Ulasan

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'  

    def create(self, validated_data):
        # Logic to create a new Menu item
        return Menu.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Logic to update an existing Menu item
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UlasanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ulasan
        fields = '__all__'  
        
class KantinSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(many=True, read_only=True)
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
    menu = MenuSerializer(many=True)