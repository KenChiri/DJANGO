# Generated by Django 5.0.3 on 2024-03-27 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0002_emergencyreport_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencyreport',
            name='photo',
            field=models.ImageField(blank=True, upload_to='media/emergency_photos/'),
        ),
    ]
