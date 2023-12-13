from django.contrib import admin
from django.utils.html import format_html

from .models import UserAvatar, UserProfile


@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    list_display = ("pk", "avatar_thumbnail", "src", "alt")
    list_display_links = ("pk", "avatar_thumbnail")
    ordering = ("pk",)

    @admin.display(description="Avatar")
    def avatar_thumbnail(self, obj):
        return format_html('<img src="{}" height="50" style="border-radius: 10%">', obj.src.url)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "avatar_thumbnail", "user", "fullName", "phone", "balance")
    list_display_links = ("pk", "avatar_thumbnail", "user", "fullName")
    search_fields = ["user__username", "fullName", "phone"]
    list_filter = ["balance"]
    ordering = ("fullName",)

    @admin.display(description="Avatar")
    def avatar_thumbnail(self, obj):
        return format_html('<a href="{0}" target="_blank"><img src="{0}" height="50" style="border-radius: 10%"></a>', obj.avatar.src.url)
