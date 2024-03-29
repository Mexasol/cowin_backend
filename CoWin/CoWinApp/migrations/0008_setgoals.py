# Generated by Django 4.2.10 on 2024-03-05 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CoWinApp', '0007_delete_setgoals'),
    ]

    operations = [
        migrations.CreateModel(
            name='SetGoals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, default='null', max_length=500, null=True)),
                ('company_name', models.CharField(blank=True, default='null', max_length=500, null=True)),
                ('location', models.CharField(blank=True, default='null', max_length=500, null=True)),
                ('job_category', models.CharField(blank=True, default='null', max_length=500, null=True)),
                ('job_speciality', models.CharField(blank=True, default='null', max_length=500, null=True)),
                ('job_keywords', models.CharField(blank=True, default='null', max_length=500, null=True)),
                ('isActive', models.BooleanField(blank=True, default=True, null=True)),
                ('userId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_feedback', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
