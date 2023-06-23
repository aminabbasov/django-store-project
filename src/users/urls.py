from django.urls import path, include
from . import views
from django.contrib.auth.views import logout_then_login

app_name = 'users'

urlpatterns = [
    path('', views.WebsiteAccountView.as_view(), name='account'),
    path('register/', views.WebsiteRegisterView.as_view(), name='register'),
    path('login/', views.WebsiteLoginView.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('change-password/', views.WebsitePasswordChangeView.as_view(), name='change-password'),         #! change "-"" to "_"
    path('edit-account-details/', views.WebsiteAccountEditView.as_view(), name='edit-account-details'),  #! change "-"" to "_"
]
