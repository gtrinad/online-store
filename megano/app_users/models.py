from django.contrib.auth.models import User
from django.db import models


def user_avatar_directory_path(instance: "UserAvatar", filename: str) -> str:
    """Generate file path for user avatar."""

    return "avatars/avatar_{pk}/{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class UserAvatar(models.Model):
    """Model for storing the user's avatar."""

    src = models.ImageField(
        upload_to=user_avatar_directory_path,
        default="avatars/default/default.jpg",
        verbose_name="Avatar link",
    )
    alt = models.CharField(
        max_length=128,
        default="User's default avatar",
        verbose_name="Avatar description",
    )

    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatars"

    def __str__(self) -> str:
        return "Avatar: {alt}".format(alt=self.alt)


class UserProfile(models.Model):
    """User profile model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(max_length=128, verbose_name="Full name")
    phone = models.PositiveIntegerField(
        null=True, blank=True, unique=True, verbose_name="Phone number"
    )
    balance = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name="Balance"
    )
    avatar = models.ForeignKey(
        UserAvatar,
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_profile",
        verbose_name="Avatar",
    )

    class Meta:
        ordering = ["fullName"]
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        return "{user}".format(user=self.user)
