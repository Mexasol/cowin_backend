# Generated by Django 4.2.13 on 2024-05-17 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CoWinApp', '0004_alter_settingslauncherpropilot_company_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('type', models.CharField(blank=True, max_length=1000, null=True)),
                ('credits', models.CharField(blank=True, max_length=500, null=True)),
                ('InterviewCoPilot', models.CharField(blank=True, max_length=500, null=True)),
                ('CodingMathsCoPilot', models.CharField(blank=True, max_length=500, null=True)),
                ('AILLM', models.CharField(blank=True, max_length=500, null=True)),
                ('Performance', models.CharField(blank=True, max_length=500, null=True)),
                ('Latency', models.CharField(blank=True, max_length=500, null=True)),
                ('Resumegenerated', models.CharField(blank=True, max_length=500, null=True)),
                ('CoverLettergenerated', models.CharField(blank=True, max_length=500, null=True)),
                ('Flashcard', models.CharField(blank=True, max_length=500, null=True)),
                ('MockInterview', models.CharField(blank=True, max_length=500, null=True)),
                ('Mentorship', models.CharField(blank=True, max_length=500, null=True)),
                ('MenteeNetworking', models.CharField(blank=True, max_length=500, null=True)),
                ('HelpSupport', models.CharField(blank=True, max_length=500, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentCustId', models.CharField(blank=True, max_length=1000, null=True)),
                ('paymentId', models.CharField(blank=True, max_length=1000, null=True)),
                ('paymentPlan', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, max_length=1000, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('description', models.CharField(blank=True, max_length=3000, null=True)),
                ('credits', models.CharField(blank=True, max_length=500, null=True)),
                ('noofmin', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('startDate', models.DateTimeField(auto_now_add=True, null=True)),
                ('endDate', models.DateTimeField(auto_now_add=True, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('updatedAt', models.DateTimeField(blank=True, null=True)),
                ('packegeId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CoWinApp.packages')),
                ('userId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_payment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]