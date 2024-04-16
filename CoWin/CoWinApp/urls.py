from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "CoWinApp"

urlpatterns = [

                  # ------------- AUTHENTICATIONS SECTION ---------------

                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

                  path("auth/signup/", views.postauthuser, name="authuser"),
                  path("auth/login/", views.loginUser, name="authuserlogin"),
                  path("auth-social/", views.register_or_login, name="register_or_login"),
                  path("auth/update/password/", views.update_password, name="update_password"),
                  path("auth/update/profile-image/", views.update_profile, name="update_profile"),
                  path('auth/delete/profile-image/', views.delete_profile_image, name='delete_profile_image'),
                  path("auth/delete/user/", views.delete_user, name="delete_user"),

                  # ------------- FORGET PASSWORD SECTION ---------------

                  path("forget-password/", views.ForgetPasswordView,
                       name="forget-password"),
                  path('verify-opt/', views.VerifyOTP, name="verify-otp"),
                  path("reset-password/", views.ResetPasswordView, name="reset-password"),

                  # ---------------- SET GOALS SECTION ------------------

                  path("subdomain1/set-goals", views.set_goals, name="set_goals"),
                  path("subdomain1/edit-goals", views.edit_goals, name="edit_goals"),
                  path("subdomain1/get-all-goals", views.get_all_goals, name="get_all_goals"),
                  path("subdomain1/inactive-goals", views.get_archived_goals, name="inactive_goals"),
                  path("subdomain1/active-goals", views.get_unarchived_goals, name="active_goals"),
                  path("subdomain1/delete-goals", views.delete_goal, name="delete_goal"),

                  # ---------------- RESUME SECTION ------------------

                  path("subdomain1/upload-resume", views.UploadResume, name="upload_resume"),
                  path("subdomain1/update/resume/<int:resume_id>", views.UpdateResume, name="update_resume"),
                  path("subdomain1/get-all-resume/", views.GetAllResume, name="get_all_resume"),
                  path('subdomain1/download-resume/<int:pk>/', views.download_resume, name='download_resume'),
                  path("subdomain1/delete-resume/", views.DeleteResume, name="delete_resume"),

                  # ---------------- COVER LETTER SECTION ------------------

                  path("subdomain1/upload-coverletter", views.UploadCoverLetter, name="upload_cover_letter"),
                  path("subdomain1/update/coverletter/<int:coverletter>", views.UpdateCoverLetter,
                       name="update_cover_letter"),
                  path('subdomain1/download-cover-letter/<int:pk>/', views.download_cover_letter,
                       name='download_cover_letter'),
                  path("subdomain1/get-all-coverletter/", views.GetAllCoverLetter, name="get_all_cover_letter"),
                  path("subdomain1/delete-coverletter/", views.DeleteCoverLetter, name="delete_cover_letter"),

                  # ----------------- Flash Card SECTION ------------------
                  path("subdomain1/flashcard/", views.FlashCardQA, name="flashcard"),

                  # ----------------- Free Mock Interview SECTION ------------------

                  # path("FreeMockInterviews/", views.FreeMockInterviews, name="FreeMockInterview"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
