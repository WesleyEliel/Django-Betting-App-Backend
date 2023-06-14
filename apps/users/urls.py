# -*- coding: utf-8 -*-
"""
Created on June 8, 2023

@author:
    Wesley Eliel MONTCHO, alias DevBackend7
"""


from django.urls import path, include
from apps.users import views

from apps.users.router import router

urlpatterns = [
    # path("auth/knox/", include('knox.urls')),
    path("auth/register/", views.RegisterView.as_view()),
    path("auth/login/", views.LoginView.as_view()),
    path("auth/logout/", views.LogoutView.as_view()),
    path("auth/logout-all/", views.LogoutAllView.as_view()),
    path("auth/update-password/", views.ChangePasswordView.as_view()),
    path("accounts/me/", views.RetrieveUserView.as_view()),
    path("accounts/me/update/", views.UpdateUserInfosView.as_view()),

]
urlpatterns += router.urls
