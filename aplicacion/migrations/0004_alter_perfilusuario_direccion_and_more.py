# Generated by Django 5.1.5 on 2025-02-03 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0003_alter_producto_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilusuario',
            name='direccion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
