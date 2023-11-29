from django.db import models, transaction
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
        pemilik, _ = cls.objects.get_or_create(
            user_information=user_information,
            defaults={'kantin': None}  # Adjust the defaults as needed
        )

        if not pemilik:
            raise AuthenticationException("PemilikKantin with given user information does not exist.")

        # Check if the pemilik already has a kantin
        if pemilik.kantin:
            raise IntegrityErrorException("This PemilikKantin already has a registered Kantin.")

        with transaction.atomic():

            # Create Kantin instance
            kantin = Kantin.objects.create(**kantin_data)

            # Link UserInformation with Kantin
            pemilik.kantin = kantin
            pemilik.save()

        return kantin