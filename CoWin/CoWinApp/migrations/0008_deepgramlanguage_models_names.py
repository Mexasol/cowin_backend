# Generated by Django 4.2.13 on 2024-05-15 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoWinApp', '0007_propilotsettings_delete_referral'),
    ]

    operations = [
        migrations.AddField(
            model_name='deepgramlanguage',
            name='models_names',
            field=models.TextField(blank=True, null=True),
        ),
    ]
