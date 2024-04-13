from django.contrib import admin
from .models import SetGoals, Users, ResumeCV, CoverLetter, AICategory, AISubcategory, FlashCardInterviewQuestion

admin.site.site_header = 'Cowin Admin'


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    # def get_list_display1(self, request):
    #     return [field.name for field in Users._meta.fields]
    list_display = ('userId', 'profile')


@admin.register(SetGoals)
class SetGoalsAdmin(admin.ModelAdmin):
    # def get_list_display(self, request):
    #     return [field.name for field in SetGoals._meta.fields]
    list_display = ('userId', 'company_name', 'position', 'isArchived')
    search_fields = ('userId', 'company_name', 'position', 'location', 'job_category', 'job_speciality', 'job_keywords')
    list_filter = ('isArchived', 'job_category', 'job_speciality')


@admin.register(ResumeCV)
class ResumeCVAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'CV_document', 'upload_date', 'isPrimary')
    search_fields = ('CV_document', 'upload_date', 'isPrimary')
    list_filter = ('CV_document', 'upload_date', 'isPrimary')


@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ('userId', 'Letter_document', 'upload_date', 'isPrimary')
    search_fields = ('Letter_document', 'upload_date', 'isPrimary')
    list_filter = ('Letter_document', 'upload_date', 'isPrimary')


@admin.register(AICategory)
class AICategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(AISubcategory)
class AISubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(FlashCardInterviewQuestion)
class FlashCardInterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'date_added', 'category', 'subcategory')
    search_fields = ('question', 'answer', 'date_added', 'category', 'subcategory')
    list_filter = ('question', 'answer', 'date_added', 'category', 'subcategory')
