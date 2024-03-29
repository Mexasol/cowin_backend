from django.contrib.auth.models import User, Group
from .models import SetGoals,ResumeCV,CoverLetter,FlashCardInterviewQuestion,AICategory,AISubcategory
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username', 
            'email',
            'password',
            'is_superuser',
            'first_name',
            'last_name',
            'date_joined',
            'is_active'
            ]
        
    def create(self, validated_data):
        
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_superuser =validated_data['is_superuser'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
def get_tokens_for_user(user_id, user, profile):
    refresh = RefreshToken.for_user(user_id)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': user,
        'profile': profile,
    }
    

class SetGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetGoals
        fields = [
            'userId',
            'id',
            'position', 
            'company_name', 
            'location', 
            'job_category', 
            'job_speciality', 
            'job_keywords', 
            'isArchived'
            ]



class ResumeCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeCV
        fields = [
            'userId',
            'id',
            'CV_document', 
            'upload_date', 
            'isPrimary',
            'isActive',
            ]
        extra_kwargs = {
            'isActive': {'required': False},
        }


class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = [
            'userId',
            'id',
            'Letter_document', 
            'upload_date', 
            'isPrimary',
            'isActive',
            ]

class FlashCardInterviewQuestionsSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    subcategory_name = serializers.SerializerMethodField()

    class Meta:
        model = FlashCardInterviewQuestion
        fields = [
            'id',
            'question',
            'answer',
            'category_name',
            'subcategory_name',
        ]

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_subcategory_name(self, obj):
        return obj.subcategory.name if obj.subcategory else None


