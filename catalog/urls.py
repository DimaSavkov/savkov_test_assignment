#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers
from catalog import views

router = routers.DefaultRouter()
router.register(r'domains', views.DomainViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
