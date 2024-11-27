# Generated by Django 3.2.25 on 2024-11-27 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='imagenes',
            fields=[
                ('imgCodigo', models.CharField(choices=[('IMG-1', 'IMG-1'), ('IMG-2', 'IMG-2'), ('IMG-3', 'IMG-3'), ('IMG-4', 'IMG-4'), ('IMG-5', 'IMG-5'), ('IMG-6', 'IMG-6')], max_length=5, primary_key=True, serialize=False)),
                ('imgNombre', models.CharField(max_length=255)),
                ('imgTipo', models.CharField(max_length=50)),
                ('imgTamanio', models.IntegerField()),
                ('imgContenido', models.BinaryField()),
            ],
        ),
    ]
