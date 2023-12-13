from django.urls import path

from app_users.views import SignUpView, SignOutView, SignInView, ProfileView, AvatarUpdateView, PasswordUpdateView

app_name = "app_users"


urlpatterns = [
    path("sign-in", SignInView.as_view(), name="login"),
    path("sign-up", SignUpView.as_view(), name="register"),
    path("sign-out", SignOutView.as_view(), name="logout"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("profile/avatar", AvatarUpdateView.as_view(), name="profile_avatar_update"),
    path("profile/password", PasswordUpdateView.as_view(), name="profile_password_update"),
]
