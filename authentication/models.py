from django.db import IntegrityError, models, transaction
from django.contrib.auth.models import User
from commons.exceptions import AuthenticationException, IntegrityErrorException

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
        return f"{self.id}"
    
    @classmethod
    def registerKantin(cls, user_information, kantin_data):
        """
        Method to register a new Kantin for a PemilikKantin.
        
        :param user_information_id: ID of the UserInformation for which the Kantin is being registered.
        :param kantin_data: Dictionary containing data for the new Kantin.
        """
        
        pemilik = cls.objects.get(
            user_information=user_information,
        )
        print(pemilik.user_information)

        if not pemilik:
            raise AuthenticationException("PemilikKantin with given user information does not exist.")

        # Check if the pemilik already has a kantin
        print(pemilik.kantin)
        if pemilik.kantin is not None:
            raise IntegrityError

        with transaction.atomic():

            # Create Kantin instance
            kantin = Kantin.objects.create(nama=kantin_data.nama, 
                                           lokasi=kantin_data.lokasi,
                                           deskripsi=kantin_data.deskripsi,
                                           list_foto=kantin_data.list_foto,
                                            status_verifikasi="Pending")

            # Link UserInformation with Kantin
            pemilik.kantin = kantin
            pemilik.save()

        return kantin
    
    def editProfilKantin(self, nama, deskripsi, list_foto):
        if self.kantin:
            self.kantin.nama = nama
            self.kantin.deskripsi = deskripsi
            self.kantin.list_foto = list_foto  
            self.kantin.save()
            return self.kantin
        else:
            raise ValueError("This PemilikKantin does not have a linked Kantin.")
    
    
class Pengguna(models.Model):
    user_information = models.OneToOneField(UserInformation, on_delete=models.CASCADE, related_name='pengguna')
    kantin_favorit = models.ManyToManyField(Kantin, blank=True)

    def __str__(self):
        return f"{self.user_information.nama} - Favorite Kantins: {', '.join(str(kantin) for kantin in self.kantin_favorit.all())}"

