#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from rest_framework import serializers
from catalog.models import Domain


class DomainSerializer(serializers.HyperlinkedModelSerializer):
    """
    Domain Serializer
    """
    class Meta:
        model = Domain
        fields = ('name', 'is_private')

    def validate_name(self, value):
        """
        Validation rules:
          * Domain should start only with https://
          * Should be available on the Internet (The response from domain must to return status 200)
        """
        value = value.strip()
        domain_status = None
        STATUS_200 = 200

        # check domain name
        if not value.startswith('https://'):
            raise serializers.ValidationError('Domain should start with "https://" ')

        # check domain accessibility
        try:
            domain_status = urllib.urlopen(value).getcode()
        except IOError:
            pass
        if not domain_status == STATUS_200:
                raise serializers.ValidationError("Name or service not known")

        return value
