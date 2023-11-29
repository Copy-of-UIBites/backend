from django.db import models
from django.contrib.auth.models import User

from kantin.models import Kantin

# Create your models here.

class UserRole(models.TextChoices):
    USER = 'User'
    ADMIN = 'Admin'
    CANTEEN_OWNER = 'Pemilik Kantin'

class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='information')
    # Other Information
    nama = models.CharField(max_length=1024)
    nomor_telepon = models.CharField(max_length=14)
    is_admin = models.BooleanField(default=False)
    foto = models.URLField(blank=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    def __str__(self):
        return f"{self.user.email} - {self.nama}"
    
class PemilikKantin(models.Model):
    user_information = models.OneToOneField(UserInformation, on_delete=models.CASCADE, related_name='pemilik_kantin')
    kantin = models.OneToOneField(Kantin, on_delete=models.CASCADE, related_name='kantin', blank=True, null=True)

    def __str__(self):
        return f"{self.user.information.nama} - {self.kantin.nama}"
    
class Pengguna(models.Model):
    user_information = models.OneToOneField(UserInformation, on_delete=models.CASCADE, related_name='pengguna')
    kantin_favorit = models.ManyToManyField(Kantin, blank=True)

    def __str__(self):
        return f"{self.user_information.nama} - Favorite Kantins: {', '.join(str(kantin) for kantin in self.kantin_favorit.all())}"
