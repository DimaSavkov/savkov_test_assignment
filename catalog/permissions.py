#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """
    Custom permission to check username is 'manager'.
    """
    def has_permission(self, request, view):
        return request.user.username == 'manager'
