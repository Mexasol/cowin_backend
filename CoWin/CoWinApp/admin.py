##############################################################################
############################## Django Admin Imports ##########################
##############################################################################

from django.contrib import admin
from django.contrib.admin import ModelAdmin

##############################################################################
############################## Local Model Imports ###########################
##############################################################################

from .models import (
    SetGoals, Users, ResumeCV, CoverLetter, FlashCardCategory, FlashCardSubcategory,
    FlashCardInterviewQuestion, FreeMockInterview, ProPilotLauncher,
    AiInterviewProPilot, AiProPilotLauncher, AiCodingMaths,Payment,
    AiCodingMathsProPilotLauncher, CoverLetterTemplate, ResumeTemplate, UserDetails, 
    Images, GreetingMessage, ProgrammingLanguage, DeepgramLanguage,Contact,Packages,
    ProPilotSettings, propilottemp, Referral, BannerText,SettingsLauncherpropilot,isCompletedpropilotlaunch
)

# Set custom site header for Django admin
admin.site.site_header = 'Cowin Admin'

##############################################################################
############################## Users #########################################
##############################################################################

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('userId', 'profile', 'otp')

##############################################################################
############################## Set Goals #####################################
##############################################################################

@admin.register(SetGoals)
class SetGoalsAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'company_name', 'position', 'isActive')
    search_fields = ('userId', 'company_name', 'position', 'location')
    list_filter = ('isActive',)

##############################################################################
############################## Resume and Cover Letter #######################
##############################################################################

@admin.register(ResumeCV)
class ResumeCVAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'CV_document', 'upload_date', 'isActive')
    search_fields = ('CV_document', 'upload_date', 'isActive')
    list_filter = ('CV_document', 'upload_date', 'isActive')

@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'Letter_document', 'upload_date', 'isActive')
    search_fields = ('Letter_document', 'upload_date', 'isActive')
    list_filter = ('Letter_document', 'upload_date', 'isActive')

##############################################################################
############################## AI Categories and Subcategories ###############
##############################################################################

@admin.register(FlashCardCategory)
class AICategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(FlashCardSubcategory)
class AISubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

##############################################################################
############################## Flash Card Interview Questions ################
##############################################################################

@admin.register(FlashCardInterviewQuestion)
class FlashCardInterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'date_added', 'category', 'subcategory')
    search_fields = ('question', 'answer', 'date_added', 'category', 'subcategory')
    list_filter = ('question', 'answer', 'date_added', 'category', 'subcategory')

##############################################################################
############################## Free Mock Interviews ###########################
##############################################################################

# @admin.register(FreeMockInterview)
# class FreeMockInterview(admin.ModelAdmin):
#     list_display = ('id', 'userId', 'goals', 'InterviewTime', 'IsActive')

##############################################################################
############################## ProPilot Launcher #############################
##############################################################################

# @admin.register(ProPilotLauncher)
# class ProPilotLauncher(admin.ModelAdmin):
#     list_display = ('id', 'userId', 'resume', 'cover_letter', 'position', 'additional_details')

##############################################################################
############################## AI Interview ProPilot #########################
##############################################################################

# @admin.register(AiInterviewProPilot)
# class FreeMockInterview(admin.ModelAdmin):
#     list_display = ('id', 'userId', 'goals', 'InterviewTime', 'IsActive')

##############################################################################
############################## AI ProPilot Launcher ##########################
##############################################################################

@admin.register(AiProPilotLauncher)
class ProPilotLauncher(admin.ModelAdmin):
    list_display = ('id', 'userId', 'resume', 'cover_letter', 'position')

##############################################################################
############################## AI Coding and Maths ###########################
##############################################################################

# @admin.register(AiCodingMaths)
# class AiCodingMaths(admin.ModelAdmin):
#     list_display = ('id', 'userId', 'goals', 'IsActive')

# @admin.register(AiCodingMathsProPilotLauncher)
# class AiCodingMathsProPilot(admin.ModelAdmin):
#     list_display = ('id', 'userId', 'resume', 'cover_letter', 'programing_language', 'add_goal', 'additional_details', 'created_at')

##############################################################################
############################## Resume and Cover Letter Templates #############
##############################################################################

@admin.register(ResumeTemplate)
class ResumeTemp(admin.ModelAdmin):
    list_display = ('id', 'CV_template_Pdf', 'CV_template_Word', 'IsPaid')

@admin.register(CoverLetterTemplate)
class CoverLetterTemp(admin.ModelAdmin):
    list_display = ('id', 'CL_template_Pdf', 'CL_template_Word', 'IsPaid')


##############################################################################
############################## User Details ###################################
##############################################################################

# @admin.register(UserDetails)
# class Temperature(admin.ModelAdmin):
#     list_display = ('id', 'user', 'latest_resume', 'latest_goal', 'latest_temperature', 'updated_at')


##############################################################################
############################## Images ########################################
##############################################################################

@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image')


##############################################################################
############################## Greeting Message ###############################
##############################################################################

@admin.register(GreetingMessage)
class GreetingMessage(admin.ModelAdmin):
    list_display = ('id','message')

##############################################################################
############################## Programming Languages ########################
##############################################################################

@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ('language',)
    search_fields = ('language',)
    list_filter = ('language',)

##############################################################################
############################## Deepgram Languages  ###########################
##############################################################################

@admin.register(DeepgramLanguage)
class DeepgramLanguageAdmin(admin.ModelAdmin):
    list_display = ('id','language','models_names')
    search_fields = ('language',)
    list_filter = ('language',)

##############################################################################
############### Propilot Temperatures and Verbosity  #########################
##############################################################################

@admin.register(propilottemp)
class ProPilotTempandverbosityAdmin(admin.ModelAdmin):
    list_display = ('id', 'temp', 'verbosity')
    search_fields = ('temp',)
    list_filter = ('temp',)

##############################################################################
############################## Pro Pilot Settings  ###########################
##############################################################################

@admin.register(ProPilotSettings)
class ProPilotSettingsAdmin(admin.ModelAdmin):
    list_display = ('user','verbosity', 'deepgram_language', 'programming_language', 'tran_delay', 'propilot_temp')
    search_fields = ('user',)
    list_filter = ('user',)

##############################################################################
############################## Referral code  ################################
##############################################################################

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('id','code', 'user', 'created_at')
    search_fields = ('code', 'user')
    list_filter = ('code', 'user')

##############################################################################
############################## Banner Text  ##################################
##############################################################################

@admin.register(BannerText)
class BannerTextAdmin(admin.ModelAdmin):
    list_display = ('id','text')
    search_fields = ('text',)
    list_filter = ('text',)

##############################################################################
############################## ProPilot settings Launcher  ###################
##############################################################################

@admin.register(SettingsLauncherpropilot)
class ProPilotSettingsLauncherAdmin(admin.ModelAdmin):
    list_display = ('id','user')
    search_fields = ('user',)
    list_filter = ('user',)

##############################################################################
################################## Packages  #################################
##############################################################################
@admin.register(Packages)
class PackagesAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'price')
    search_fields = ('title',)
    list_filter = ('title',)

##############################################################################
############################### Contact Us  ##################################
##############################################################################

@admin.register(Contact)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'subject', 'message', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('name', 'email', 'subject', 'message')

##############################################################################
####################################  Payment  ###############################
##############################################################################

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','email','userId', 'packegeId', 'paymentCustId', 'paymentId', 'paymentPlan', 'type')
    search_fields = ('email', 'amount', 'packegeId', 'type')
    list_filter = ('email', 'amount', 'packegeId', 'type')

@admin.register(isCompletedpropilotlaunch)
class isCompletedpropilotlaunchAdmin(admin.ModelAdmin):
    list_display = ('id','user')
    search_fields = ('user',)
    list_filter = ('user',)
