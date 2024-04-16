from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Users(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='Users')
    profile = models.ImageField(null=True, blank=True, upload_to='images/')
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)

    def is_otp_expired(self):
        if self.otp_expiry:
            return timezone.now() > self.otp_expiry
        return True

    def set_otp_expiry(self, expiry_duration):
        self.otp_expiry = timezone.now() + timedelta(seconds=expiry_duration)


class SetGoals(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='User_Set_Goals')
    position = models.CharField(max_length=500, null=True, blank=True, default='null')
    company_name = models.CharField(max_length=500, null=True, blank=True, default='null')
    location = models.CharField(max_length=500, null=True, blank=True, default='null')
    isActive = models.BooleanField(null=True, blank=True, default=True)

    def __str__(self):
        return self.company_name


class ResumeCV(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='User_CV')
    CV_document = models.FileField(upload_to='CV_Documents/', null=True, blank=True)
    upload_date = models.DateField(auto_now_add=True, null=True, blank=True)
    isActive = models.BooleanField(null=True, blank=True, default=True)


class CoverLetter(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='User_CoverLetter')
    Letter_document = models.FileField(upload_to='CL_Documents/', null=True, blank=True)
    upload_date = models.DateField(auto_now_add=True, null=True, blank=True)
    isActive = models.BooleanField(null=True, blank=True, default=True)


class AICategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AISubcategory(models.Model):
    category = models.ForeignKey(AICategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FlashCardInterviewQuestion(models.Model):
    question = models.CharField(max_length=500, null=True, blank=True, default='null')
    answer = models.TextField(max_length=1000, null=True, blank=True, default='null')
    date_added = models.DateField(auto_now_add=True)
    category = models.ForeignKey(AICategory, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(AISubcategory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question


class FreeMockInterview(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='FreeMockInterviews')
    goals = models.ForeignKey(SetGoals, on_delete=models.CASCADE, null=True, blank=True, related_name='mock_interview_goals')
    InterviewTime = models.DateTimeField(null=True, blank=True)
