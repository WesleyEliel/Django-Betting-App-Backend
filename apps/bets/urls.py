# -*- coding: utf-8 -*-
"""
Created on June 13, 2023

@author:
    Wesley Eliel MONTCHO, alias DevBackend7
"""


from django.urls import path
from apps.bets.router import router

urlpatterns = [
    # path("auth/register/", views.RegisterView.as_view()),
]
urlpatterns += router.urls
