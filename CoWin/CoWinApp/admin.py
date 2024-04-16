from django.contrib import admin
from .models import SetGoals, Users, ResumeCV, CoverLetter, AICategory, AISubcategory, FlashCardInterviewQuestion, \
    FreeMockInterview

admin.site.site_header = 'Cowin Admin'


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    # def get_list_display1(self, request):
    #     return [field.name for field in Users._meta.fields]
    list_display = ('userId', 'profile', 'otp')


@admin.register(SetGoals)
class SetGoalsAdmin(admin.ModelAdmin):
    # def get_list_display(self, request):
    #     return [field.name for field in SetGoals._meta.fields]
    list_display = ('userId', 'company_name', 'position', 'isActive')
    search_fields = ('userId', 'company_name', 'position', 'location')
    list_filter = ('isActive',)


@admin.register(ResumeCV)
class ResumeCVAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'CV_document', 'upload_date', 'isActive')
    search_fields = ('CV_document', 'upload_date', 'isActive')
    list_filter = ('CV_document', 'upload_date', 'isActive')


@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ('userId', 'Letter_document', 'upload_date', 'isActive')
    search_fields = ('Letter_document', 'upload_date', 'isActive')
    list_filter = ('Letter_document', 'upload_date', 'isActive')


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


@admin.register(FreeMockInterview)
class FreeMockInterview(admin.ModelAdmin):
    list_display = ('userId', 'goals', 'InterviewTime')
