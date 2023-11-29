from django.contrib import admin

from .models import PemilikKantin, UserInformation

admin.site.register(UserInformation)
admin.site.register(PemilikKantin)