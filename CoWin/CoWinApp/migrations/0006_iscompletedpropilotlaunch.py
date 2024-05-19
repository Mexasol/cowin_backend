# Generated by Django 4.2.13 on 2024-05-19 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CoWinApp', '0005_contact_packages_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='isCompletedpropilotlaunch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=500, null=True)),
                ('company', models.CharField(blank=True, max_length=500, null=True)),
                ('interviewtime', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]