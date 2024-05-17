from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views

app_name = "CoWinApp"

urlpatterns = [

                  # ------------- AUTHENTICATIONS SECTION ---------------
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

                  path("auth/signup/", views.postauthuser, name="authuser"),
                  path("auth/login/", views.loginUser, name="authuserlogin"),
                  path('auth/userprofile/', views.user_profile_api, name='user_profile_api'),
                  path("auth-social/", views.register_or_login, name="register_or_login"),
                  path("auth/update/password/", views.update_password, name="update_password"),
                  path("auth/update/profile-image/", views.update_profile, name="update_profile"),
                  path('auth/delete/profile-image/', views.delete_profile_image, name='delete_profile_image'),
                  path("auth/delete/user/", views.delete_user, name="delete_user"),
                  path("auth/check-user-status/", views.check_user_status, name="check_user_status"),

                  # ------------- FORGET PASSWORD SECTION ---------------

                  path("forget-password/", views.ForgetPasswordView,
                       name="forget-password"),
                  path('verify-opt/', views.VerifyOTP, name="verify-otp"),
                  path("reset-password/", views.ResetPasswordView, name="reset-password"),

                  # ---------------- SET GOALS SECTION ------------------

                  path("api/set-goals/", views.set_goals, name="set_goals"),
                  path("api/edit-goals/", views.edit_goals, name="edit_goals"),
                  path("api/get-all-goals/", views.get_all_goals, name="get_all_goals"),
                  path("api/inactive-goals/", views.get_archived_goals, name="inactive_goals"),
                  path("api/active-goals/", views.get_unarchived_goals, name="active_goals"),
                  path("api/goals-status-change/", views.update_goal_status,
                       name="goals_status_inactive"),
                  path("api/delete-goals/", views.delete_goal, name="delete_goal"),

                  # ---------------- RESUME SECTION ------------------

                  path("api/upload-resume/", views.UploadResume, name="upload_resume"),
                  path("api/update/resume/", views.UpdateResume, name="update_resume"),
                  path("api/get-all-resume/", views.GetAllResume, name="get_all_resume"),
                  path('api/download-resume/', views.download_resume, name='download_resume'),
                  path("api/delete-resume/", views.DeleteResume, name="delete_resume"),

                  # ---------------- COVER LETTER SECTION ------------------

                  path("api/upload-coverletter/", views.UploadCoverLetter, name="upload_cover_letter"),
                  path("api/update/coverletter/", views.UpdateCoverLetter,
                       name="update_cover_letter"),
                  path('api/download-cover-letter/', views.download_cover_letter,
                       name='download_cover_letter'),
                  path("api/get-all-coverletter/", views.GetAllCoverLetter, name="get_all_cover_letter"),
                  path("api/delete-coverletter/", views.DeleteCoverLetter, name="delete_cover_letter"),

                  # ----------------- Flash Card SECTION ------------------
                  path("api/flashcard/", views.FlashCardQA, name="flashcard"),

                  # ----------------- Lookup SECTION ------------------
                  path('api/get-userset-goals-lookup/', views.GetUserSetGoalsLookup,
                       name="GetUserSetGoalsLookup"),
                  path('api/resume-lookup/', views.GetUserResumeLookup,
                       name="GetUserResumeLookup"),
                  path('api/cover-letter-lookup/', views.GetUserCoverLetterLookup,
                       name="GetUserCoverLetterLookup"),
                  path('api/position-lookup/', views.GetUserPositionLookup,
                       name="GetUserPositionLookup"),
                  

                  # ----------------- Free Mock Interview SECTION ------------------
                  path('api/free-mock-creation/', views.FreeMockCreation, name="FreeMockCreation"),
                  path('api/free-mock-creation-complete/', views.FreeMockCompletion,
                       name="FreeMockCompletion"),
                  path('api/free-mock-get/', views.FreeMockGetDetails, name="FreeMockGet"),

                  # ----------------- ProLauncher SECTION ------------------
                  path("api/pro-luancher-create/", views.ProPilotLauncherCreation, name="proluancher_creattion"),
                  path("api/Pro-luancher-data/", views.ProPilotLauncherViewGet, name="proluancher_get_data"),

                  # ----------------- AI Interview SECTION ------------------
                  path('api/ai-Interview-creation/', views.AiInterviewCreation, name="AiInterviewCreation"),
                  path('api/ai-set-status/', views.Ai_Set_Status,
                       name="SetStatusCompletion"),
                  path('api/ai-get-details/', views.AiInterviewGetDetails, name="FreeMockGet"),

                  # ----------------- ProLauncher SECTION ------------------
                  path("api/ai-pro-luancher-create/", views.AiProPilotLauncherCreation,
                       name="AiProPilotLauncherCreation"),

                  path("api/ai-pro-luancher-data/", views.AiProPilotLauncherGet, name="AiProPilotLauncherGet"),

                  # ----------------- Ai Coding Maths SECTION ------------------
                  path('api/ai-coding-maths-creation/', views.AiCodingMathsCreation, name="AiCodingMaths"),
                  path('api/ai-coding-maths-set-status/', views.AiCodingMaths_Set_Status,
                       name="SetStatusCompletion"),
                  path('api/ai-coding-maths-get-details/', views.AiCodingMathsGetDetails, name="AiCodingMaths"),

                  # ----------------- ProLauncher SECTION ------------------
               #    path("api/aicodingmaths-pro-luancher-create/", views.AiCodingMathsProPilotCreation,
               #         name="AiCodingMathsProPilotCreation"),
               #    path('api/ai-coding-maths-pro-luancher-data/', views.AiCodingMathsProPilotGet,
               #         name="AiCodingMaths"),

                  # ----------------- Resume Templates SECTION ------------------
                  path('api/resume-template/', views.ResumeTemplates, name="Resume-Template-All"),
                  path('api/resume-template-get/', views.SingleResumeTemplates, name="Resume-Template-Single"),
                  path('api/resume-template-add/', views.ResumeTemplateAdd, name="Resume-Template-add"),

                  # ----------------- CoverLetter Templates SECTION ------------------
                  path('api/cover-letter-template/', views.CoverLetterTemplates,
                       name="Cover-Letter-Template-All"),
                  path('api/cover-letter-template-single/', views.SingleCoverletterTemplates,
                       name="Cover-Letter-Template-Single"),
                  path('api/cover-letter-template-add/', views.CoverLetterTemplateAdd,
                       name="Cover-Letter-Template-Add"),

                  # ----------------- OCR  SECTION ------------------
                  path('api/perform-ocr/', views.Perform_OCR_Api, name='perform_ocr_image_to_text'),
                  path('api/user-detail/', views.UserData, name="UserDetails"),
                  path('api/delete-user-details/', views.DeleteUserDetails, name="Delete"),


                  # ----------------- greeting SECTION ------------------
                  path('api/greeting/', views.get_greeting, name='greeting'),
                  
                  # ----------------- programming Language SECTION ------------------
                  path('api/languages/', views.language_list, name='language-list'),
                  path('api/languages/<int:pk>/', views.language_detail, name='language-detail'),

                  # ----------------- Deepgram SECTION ------------------
                  path('api/deepgram/', views.deepgram_language_list, name="Deepgram"),
                  path('api/deepgram/<int:pk>/', views.deepgram_language_detail, name="Deepgram"),

                  # ----------------- Pro Pilot Settings SECTION ------------------
                  path('api/pro-pilot-settings/', views.pro_pilot_settings_list, name="pro_pilot_settings"),
                  path('api/pro-pilot-settings/<int:pk>/', views.pro_pilot_settings_detail, name="pro_pilot_settings"),

                  # ----------------- Referral ------------------
                  path('api/referral/', views.verify_referral, name='verify_referral'),
                  path('api/generate-referral-link/', views.generate_referral_link, name='generate_referral_link'),

                  # ----------------- banner text ------------------
                  path('api/home-banner-text/', views.get_banner_text, name='get_banner_text'),

                  # ----------------- propilot-settings ------------------
                  path('api/propilot-settings/', views.propilot_settings, name='propilot-settings'),
                  path('api/pro-pilot-temperatures-list/', views.pro_pilot_temperatures_list, name='pro_pilot_temperatures_list'),

                  # ----------------- Contact ------------------
                  path('api/contact/', views.contact_create, name='contact-create'),

                  # ----------------- Package ------------------
                  path("api/getallpackages/", views.getPackages, name="getallpackages"),
                  path("api/getsinglepackage/<int:package_id>/", views.getPackagesbyid, name="getsinglepackage"),

                  # ----------------- Payment ------------------
                  path('api/payments/', views.create_payment, name='create_payment'),
                  path('api/getPayment/', views.getPayment, name='get_payment'),
    






              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
