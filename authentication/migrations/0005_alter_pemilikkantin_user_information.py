# Generated by Django 4.2.1 on 2023-11-29 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_pemilikkantin_kantin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pemilikkantin',
            name='user_information',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pemilik_kantin', to='authentication.userinformation'),
        ),
    ]
