from django.contrib.auth.models import User

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from catalog.models import Domain
from catalog.serializers import DomainSerializer
from catalog.permissions import IsManager


class DomainViewSet(viewsets.ModelViewSet):
    """
        API that allows domains to be viewed or created
         * Authenticated user can get any domain(s)
         * AnonymousUser can get only domain(s) where is_private is False
         * Only user with username 'manager' can create domain (see IsManager())
    """
    queryset = Domain.objects.all().order_by('-id')
    serializer_class = DomainSerializer

    def get_permissions(self):
        # allow 'manager' user to create via POST
        if self.request.method == 'POST':
            return (IsManager(), )
        else:
            return (permissions.AllowAny(), )

    def get_queryset(self):
        # authenticated users can view all Domains
        # guests can get only domain(s) where is_private is False
        if self.request.user.is_authenticated():
            return Domain.objects.all().order_by('-id')
        else:
            return Domain.objects.filter(is_private=False).order_by('-id')
