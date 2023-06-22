# -*- coding: utf-8 -*-
"""
Created on June 6, 2023

@author:
    Wesley Eliel MONTCHO, alias DevBackend7
"""

from rest_framework.routers import DefaultRouter

from apps.users.views import TransactionViewSet

router = DefaultRouter()
# router.register(r"", viewset, basename="")
router.register(r"transactions", TransactionViewSet, basename="TransactionViewSet")
urls_patterns = router.urls
