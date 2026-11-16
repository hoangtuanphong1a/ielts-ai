from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Your current password is incorrect.")
        return value

    def validate(self, attrs):
        validate_password(attrs["new_password"], self.context["request"].user)
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["role", "target_band", "exam_date", "daily_minutes"]
        read_only_fields = ["role"]  # vai trò chỉ admin đổi (qua Django admin)

    def validate_target_band(self, value):
        # Band IELTS đi theo bước 0.5
        if value is not None and (value * 2) % 1 != 0:
            raise serializers.ValidationError("Band must be a multiple of 0.5 (for example 6.5 or 7.0).")
        return value


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined", "profile"]
        read_only_fields = ["id", "username", "date_joined"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        instance = super().update(instance, validated_data)
        if profile_data:
            profile = instance.profile
            for key, value in profile_data.items():
                setattr(profile, key, value)
            profile.save()
        return instance
