from django.contrib.auth.views import logout_then_login
from django.urls import path

from users import views


app_name = "users"

urlpatterns = [
    path("", views.UsersAccountView.as_view(), name="account"),
    path("register/", views.UsersRegisterView.as_view(), name="register"),
    path("login/", views.UsersLoginView.as_view(), name="login"),
    path("logout/", logout_then_login, name="logout"),
    path("change-password/", views.UsersPasswordChangeView.as_view(), name="change-password"),  #! change "-"" to "_"
    path(
        "edit-account-details/", views.UsersAccountEditView.as_view(), name="edit-account-details"
    ),  #! change "-"" to "_"
]
