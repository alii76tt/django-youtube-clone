from django.urls import path
from .views import *

app_name = "account"
urlpatterns = [
    path("login/", loginView, name="login"),
    path("sign_up/", signUp, name="signUp"),
    path("logout/", logoutView, name="logout"),

    # user
    path("profile/", userProfile, name="userProfile"),
    path("update/profile/", updateUserProfile, name="updateUserProfile"),
    path("change/password/", changeUserPassword, name="changeUserPassword"),
]
