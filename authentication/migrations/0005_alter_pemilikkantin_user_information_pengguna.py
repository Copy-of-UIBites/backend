# Generated by Django 4.2.1 on 2023-11-29 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kantin', '0002_alter_kantin_list_foto_alter_kantin_lokasi_and_more'),
        ('authentication', '0004_alter_pemilikkantin_kantin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pemilikkantin',
            name='user_information',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pemilik_kantin', to='authentication.userinformation'),
        ),
        migrations.CreateModel(
            name='Pengguna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kantin_favorit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kantin.kantin')),
                ('user_information', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pengguna', to='authentication.userinformation')),
            ],
        ),
    ]
