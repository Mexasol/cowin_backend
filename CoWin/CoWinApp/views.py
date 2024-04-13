import random
from .models import Users, SetGoals, ResumeCV, CoverLetter, FlashCardInterviewQuestion
from .serializers import UserSerializer, SetGoalsSerializer, ResumeCVSerializer, \
    CoverLetterSerializer, FlashCardInterviewQuestionsSerializer, ForgetPasswordSerializer, ResetPasswordSerializer
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from asgiref.sync import sync_to_async
from django.core.files.storage import default_storage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .utils import send_mail_using_smtp
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

"""
-----------------------------------------------------
------------- AUTHENTICATIONS SECTION ---------------
-----------------------------------------------------
"""


@sync_to_async
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def postauthuser(request):
    try:
        fullName = request.data.get('fullname')
        first_name, last_name = fullName.split(' ', 1) if ' ' in fullName else (fullName, '')
        email = request.data.get('email')
        password = request.data.get('password')
        is_superuser = request.data.get('is_superuser')
        is_superuser = is_superuser if is_superuser is not None else False

        profile_value = request.data.get('profile')

        # Check if the user with the provided email already exists
        user = User.objects.filter(email=email).first()

        if user:
            # User already exists
            user_instance = Users.objects.get(userId=user.id)

            # Set the 'profile' value only if provided in the request
            if profile_value is not None:
                user_instance.profile = profile_value
                user_instance.save()
            return Response({'error': f'User with this email already exist.'}, status=status.HTTP_400_BAD_REQUEST)



        else:
            user_data = {
                'username': email,
                'email': email,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'is_superuser': is_superuser,
            }
            serializer = UserSerializer(data=user_data)

            if serializer.is_valid():
                user = serializer.create(serializer.validated_data)
                Users.objects.get_or_create(userId=user)
                user_id = user.id

                # Set the 'profile' value only if provided in the request
                if profile_value is not None:
                    user_instance = Users.objects.get(userId=user_id)
                    user_instance.profile = profile_value
                    user_instance.save()

                # Get tokens for new user
                # data = get_tokens_for_user(user, user_id, profile_value)

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"response": f"Something went wrong: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@sync_to_async
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def loginUser(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            user_id = User.objects.filter(username=username).values()

            try:
                user_instance = Users.objects.get(userId=user_id[0]['id'])
                profile_value = user_instance.profile.url if user_instance.profile else None
            except Users.DoesNotExist:
                profile_value = "unknown"

            refresh = RefreshToken.for_user(user)

            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user_id[0]).data,
                'profile': profile_value,
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response({"error": "Invalid username or password"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        error_message = f"Something went wrong: {e}"
        return Response({"response": error_message}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def register_or_login(request):
    username = request.data.get('username')
    email = request.data.get('email')

    # Check if user with given email already exists
    user = User.objects.filter(email=email).first()
    if user:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response({
            'message': 'User with this email already exists.',
            'username': user.username,
            'email': user.email,
            'access_token': str(access),
            'refresh_token': str(refresh)
        })
    else:
        # User doesn't exist, create a new user
        user = User.objects.create_user(username=username, email=email)
        # Create a corresponding entry in the Users table
        Users.objects.get_or_create(userId=user)
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response({
            'username': user.username,
            'email': user.email,
            'access_token': str(access),
            'refresh_token': str(refresh)
        })


@sync_to_async
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_password(request):
    try:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user_id_from_token = access_token['user_id']
            user = User.objects.get(id=user_id_from_token)
        except Exception as e:
            return Response({"error": f"You are not authorized {e}"}, status=status.HTTP_400_BAD_REQUEST)

        current_password = request.data.get('current_password', None)
        new_password = request.data.get('new_password', None)
        confirm_new_password = request.data.get('confirm_new_password', None)

        if current_password == new_password:
            return Response({"error": "New password should be different from the current password."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not check_password(current_password, user.password):
            return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_new_password:
            return Response({"error": "New password and confirm new password does not match."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Something went wrong {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@sync_to_async
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user_id_from_token = access_token['user_id']
            user = User.objects.get(id=user_id_from_token)
        except Exception as e:
            return Response({"error": f"You are not authorized {e}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            users_instance = Users.objects.get(userId=user)
            users_fields_to_update = ['profile']
            for field in users_fields_to_update:
                if field in request.data:
                    setattr(users_instance, field, request.data[field])
            users_instance.save()
        except Users.DoesNotExist:
            pass

        return Response({"response": "Profile Picture Updated Successfully"}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"response": f"Something went wrong {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@sync_to_async
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile_image(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        access_token = AccessToken(token)
        user_id_from_token = access_token['user_id']
        user = User.objects.get(id=user_id_from_token)
    except Exception as e:
        return Response({"error": f"You are not authorized {e}"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        users_instance = Users.objects.get(userId=user)
        if users_instance.profile:
            image_path = users_instance.profile.path
            default_storage.delete(image_path)
            users_instance.profile = None
            users_instance.save()

            return Response({"response": "Profile Picture Deleted Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"response": "No profile picture to delete"}, status=status.HTTP_204_NO_CONTENT)
    except Users.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


@sync_to_async
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    try:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user_id_from_token = access_token['user_id']
            user = User.objects.get(id=user_id_from_token)
        except Exception as e:
            return Response({"error": f"You are not authorized {e}"}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Something went wrong {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
-----------------------------------------------------
------------- FORGET PASSWORD SECTION ---------------
-----------------------------------------------------
"""


@api_view(['POST'])
def ForgetPasswordView(request):
    serializer = ForgetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data["email"]

    # Get the user with the provided email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
    user_instance = Users.objects.get(userId=user.id)
    otp = random.randint(111111, 999999)
    expiry_time = timezone.now() + timedelta(hours=24)
    expiry_duration = (expiry_time - timezone.now()).total_seconds()

    # Store OTP in the user's OTP field
    user_instance.otp = otp
    user_instance.set_otp_expiry(expiry_duration)
    user_instance.save()

    # Compose email data
    email_data = {
        "from": settings.EMAIL_HOST_USER,
        "subject": "Password Reset OTP",
        "recipient": [email],
    }
    send_mail_using_smtp(otp, email_data)

    return Response({"data": f"Reset password OTP has been sent to you on {email}"})


@api_view(["POST"])
def VerifyOTP(request):
    email = request.data["email"]
    otp = request.data["otp"]
    try:
        user = User.objects.filter(email=email).first()
    except User.DoesNotExist:
        return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if user:
        # User already exists
        encoded_user = urlsafe_base64_encode(force_bytes(user.email))
        user_instance = Users.objects.get(userId=user.id)
        if user_instance.otp != otp:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the OTP has expired
        if user_instance.is_otp_expired():
            return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

        # OTP is valid and not expired
        return Response({"key": encoded_user, "message": "OTP verified successfully"},
                        status=status.HTTP_200_OK)

    # Handle case where user does not exist
    return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def ResetPasswordView(request):
    serializer = ResetPasswordSerializer(
        data=request.data, context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    return Response({"data": "Password reset successfully"})


"""
-----------------------------------------------------
---------------- SET GOALS SECTION ------------------
-----------------------------------------------------
"""


@sync_to_async
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_goals(request):
    try:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user_id_from_token = access_token['user_id']
            user = User.objects.get(id=user_id_from_token)
        except Exception as e:
            return Response({"error": "You are not authorized"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SetGoalsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userId=user)
        return Response(serializer.data)
    except:
        return Response(content={"response": "Something went wrong"}, status=status.HTTP_404_NOT_FOUND)


@sync_to_async
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_goals(request):
    try:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user_id_from_token = access_token['user_id']
            User.objects.get(id=user_id_from_token)
        except Exception as e:
            return Response({"error": "You are not authorized"}, status=status.HTTP_400_BAD_REQUEST)

        goal_id = request.data.get('goal_id')
        try:
            goals = SetGoals.objects.get(id=goal_id)
        except goals.DoesNotExist:
            return Response({"response": "Goal object not found"}, status=status.HTTP_404_NOT_FOUND)

        for field in request.data:
            setattr(goals, field, request.data[field])

        serializer = SetGoalsSerializer(goals, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"response": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@sync_to_async
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_goals(request):
    try:
        user_id = request.user.id
        goals = SetGoals.objects.filter(userId=user_id)
        serializer = SetGoalsSerializer(goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"response": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@sync_to_async
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_archived_goals(request):
    try:
        user_id = request.user.id
        active_goals = SetGoals.objects.filter(userId=user_id, isArchived=True)
        serializer = SetGoalsSerializer(active_goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"response": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@sync_to_async
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unarchived_goals(request):
    try:
        user_id = request.user.id
        active_goals = SetGoals.objects.filter(userId=user_id, isArchived=False)
        serializer = SetGoalsSerializer(active_goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"response": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@sync_to_async
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_goal(request):
    try:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user_id_from_token = access_token['user_id']
            user = User.objects.get(id=user_id_from_token)
        except Exception as e:
            return Response({"error": "You are not authorized"}, status=status.HTTP_400_BAD_REQUEST)

        goal_id = request.data.get("goal_id")
        goal_to_delete = SetGoals.objects.get(userId=user, id=goal_id)
        goal_to_delete.delete()
        return Response({"message": "Goal deleted successfully."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
-----------------------------------------------------
------------------ RESUME SECTION -------------------
-----------------------------------------------------
"""


@sync_to_async
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def UploadResume(request):
    try:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user_id_from_token = access_token['user_id']
            user = User.objects.get(id=user_id_from_token)
        except Exception as e:
            return Response({"error": f"You are not authorized {e}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ResumeCVSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userId=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"response": f"Something went wrong: {e}"}, status=status.HTTP_404_NOT_FOUND)


@sync_to_async
@api_view(['PATCH'])
@authentication_classes([])
@permission_classes([])
def UpdateResume(request, resume_id):
    try:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user_id_from_token = access_token['user_id']
            user = User.objects.get(id=user_id_from_token)
        except Exception as e:
            return Response({"error": f"You are not authorized {e}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            resume = ResumeCV.objects.get(id=resume_id, userId=user)
        except ResumeCV.DoesNotExist:
            return Response({"error": "Resume not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResumeCVSerializer(resume, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"response": f"Something went wrong: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@sync_to_async
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteResume(request):
    try:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user_id_from_token = access_token['user_id']
            user = User.objects.get(id=user_id_from_token)
        except Exception as e:
            return Response({"error": f"You are not authorized {e}"}, status=status.HTTP_400_BAD_REQUEST)

        resume_id = request.data.get("resume_id")
        resume_to_delete = ResumeCV.objects.get(userId=user, id=resume_id)
        resume_to_delete.delete()
        return Response({"message": "Resume deleted successfully."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Something went wrong {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@sync_to_async
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllResume(request):
    try:
        user_id = request.user.id
        resume = ResumeCV.objects.filter(userId=user_id)
        serializer = ResumeCVSerializer(resume, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"response": f"Something went wrong {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
-----------------------------------------------------
------------------ COVER LETTER SECTION -------------------
-----------------------------------------------------
"""


@sync_to_async
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def UploadCoverLetter(request):
    try:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user_id_from_token = access_token['user_id']
            user = User.objects.get(id=user_id_from_token)
        except Exception as e:
            return Response({"error": "You are not authorized"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CoverLetterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userId=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"response": f"Something went wrong: {e}"}, status=status.HTTP_404_NOT_FOUND)


@sync_to_async
@api_view(['PATCH'])
@authentication_classes([])
@permission_classes([])
def UpdateCoverLetter(request, coverletter):
    try:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user_id_from_token = access_token['user_id']
            user = User.objects.get(id=user_id_from_token)
        except Exception as e:
            return Response({"error": "You are not authorized"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            resume = CoverLetter.objects.get(id=coverletter, userId=user)
        except CoverLetter.DoesNotExist:
            return Response({"error": "Cover Letter not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CoverLetterSerializer(resume, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"response": f"Something went wrong: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@sync_to_async
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteCoverLetter(request):
    try:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user_id_from_token = access_token['user_id']
            user = User.objects.get(id=user_id_from_token)
        except Exception as e:
            return Response({"error": "You are not authorized"}, status=status.HTTP_400_BAD_REQUEST)

        coverletter_id = request.data.get("coverletter_id")
        coverletter_to_delete = CoverLetter.objects.get(userId=user, id=coverletter_id)
        coverletter_to_delete.delete()
        return Response({"message": "Cover Letter deleted successfully."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@sync_to_async
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllCoverLetter(request):
    try:
        user_id = request.user.id
        resume = CoverLetter.objects.filter(userId=user_id)
        serializer = CoverLetterSerializer(resume, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"response": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
-----------------------------------------------------
------------- FlashCard SECTION ---------------
-----------------------------------------------------
"""


@sync_to_async
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def FlashCardQA(request):
    try:
        # Get all the questions and answers with category and subcategory
        flashcard_qa = FlashCardInterviewQuestion.objects.all()
        serializer = FlashCardInterviewQuestionsSerializer(flashcard_qa, many=True)

        # Extracting unique category names from the serializer data
        category_names = set(item['category_name'] for item in serializer.data if item['category_name'])

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print("Error:", e)  # Print the actual error message
        return Response({"response": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
