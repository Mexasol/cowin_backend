from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken
from .models import SetGoals, ResumeCV, CoverLetter, FlashCardInterviewQuestion, AICategory, AISubcategory, Users, \
    FreeMockInterview
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

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
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


# def get_tokens_for_user(user_id, user, profile):
#     refresh = RefreshToken.for_user(user_id)
#
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#         'user': user,
#         'profile': profile,
#     }

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ("email",)


class ResetPasswordSerializer(serializers.Serializer):
    key = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        fields = (
            "key",
            "new_password",
            "confirm_password",
        )
        write_only_fields = ("key", "new_password", "confirm_password")

    def validate(self, data):
        print(data)
        encoded_user = data.get("key")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        try:
            decoded_user = urlsafe_base64_decode(encoded_user).decode()
            user = User.objects.get(email=decoded_user)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        if new_password != confirm_password:
            raise serializers.ValidationError(
                "New password and confirm password must match"
            )
        user.set_password(new_password)
        user.save()
        return data


class SetGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetGoals
        fields = [
            'userId',
            'id',
            'position',
            'company_name',
            'location',
            'isActive'
        ]


class ResumeCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeCV
        fields = [
            'userId',
            'id',
            'CV_document',
            'upload_date',
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


# class FreeMockInterviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FreeMockInterview
#         fields = '__all__'
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation.pop('goals')
#         representation['position'] = SetGoalsSerializer(instance.goals).data['position'] if instance.goals else None
#         representation['company'] = SetGoalsSerializer(instance.goals).data['company_name'] if instance.goals else None
#         return representation
