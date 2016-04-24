#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers
from catalog.views import DomainViewSet
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'api', DomainViewSet, base_name='domain')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls, namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]