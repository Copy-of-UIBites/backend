from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Kantin(models.Model):
    nama = models.TextField()
    lokasi = models.TextField()
    deskripsi = models.TextField()
    list_foto = ArrayField(models.CharField(), blank=True)
    status_verifikasi = models.TextField()

    def __str__(self):
        return self.nama
    
    @classmethod
    def searchKantin(cls, query):
        """Custom method to search Kantin by name."""
        if query:
            return cls.objects.filter(nama__icontains=query)
        else:
            return cls.objects.all()

class Menu(models.Model):
    nama = models.TextField()
    deskripsi = models.TextField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    kantin = models.ForeignKey(Kantin, on_delete=models.CASCADE, related_name='menu')

    def __str__(self):
        return self.nama

class Ulasan(models.Model):
    kantin = models.ForeignKey(Kantin, on_delete=models.CASCADE, related_name='ulasan_list')
    time_created = models.DateTimeField(auto_now_add=True)
    review = models.TextField()
    rating = models.IntegerField()
    list_foto = ArrayField(models.CharField(), blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulasan_list') 

    def __str__(self):
        return self.review
