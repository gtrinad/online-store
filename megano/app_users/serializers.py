from rest_framework import serializers

from .models import UserAvatar, UserProfile


class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = UserAvatar
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", required=True)
    avatar = AvatarSerializer()

    class Meta:
        model = UserProfile
        fields = ["fullName", "email", "phone", "avatar"]
        extra_kwargs = {
            "fullName": {"required": True},
            "phone": {"required": True},
        }

    def update(self, instance, validated_data):
        instance.fullName = validated_data.get("fullName", instance.fullName)
        instance.phone = validated_data.get("phone", instance.phone)

        # Проверяем, есть ли данные для обновления email
        user_data = validated_data.get("user", {})
        email = user_data.get("email")
        if email:
            instance.user.email = email
            instance.user.save()

        instance.save()
        return instance


class PasswordUpdateSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)

    def get_user(self):
        return self.context.get("request").user

    def validate(self, attrs):
        user = self.get_user()
        current_password = attrs["currentPassword"]

        if not user.check_password(current_password):
            raise serializers.ValidationError("Current password is incorrect.")

        return attrs
