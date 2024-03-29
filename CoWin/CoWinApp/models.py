from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    userId = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True, related_name='Users')
    profile = models.ImageField(null=True , blank=True, upload_to='images/')
    
class SetGoals(models.Model):
  userId = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True, related_name='User_Set_Goals')
  position = models.CharField(max_length=500, null=True, blank=True, default='null')
  company_name = models.CharField(max_length=500, null=True, blank=True, default='null')
  location = models.CharField(max_length=500, null=True, blank=True, default='null')
  job_category = models.CharField(max_length=500, null=True, blank=True, default='null')
  job_speciality = models.CharField(max_length=500, null=True, blank=True, default='null')
  job_keywords = models.CharField(max_length=500, null=True, blank=True, default='null')
  isArchived = models.BooleanField(null=True, blank=True, default=True)
  def __str__(self): 
    return self.company_name


class ResumeCV(models.Model):
  userId = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True, related_name='User_CV')
  CV_document = models.FileField(upload_to='CV_Documents/', null=True, blank=True)
  upload_date = models.DateField(auto_now_add=True, null=True, blank=True)
  isPrimary = models.BooleanField(null=True, blank=True, default=False)
  isActive = models.BooleanField(null=True, blank=True, default=True)
  

class CoverLetter(models.Model):
  userId = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True, related_name='User_CoverLetter')
  Letter_document = models.FileField(upload_to='CL_Documents/', null=True, blank=True)
  upload_date = models.DateField(auto_now_add=True, null=True, blank=True)
  isPrimary = models.BooleanField(null=True, blank=True, default=False)
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



