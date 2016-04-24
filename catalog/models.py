#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


class Domain(models.Model):
    """
        Model to store domain names and privacy flag
    """
    name = models.CharField(max_length=255, unique=True, verbose_name='domain name')
    is_private = models.BooleanField(default=False, verbose_name='domain is private')

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        app_label = 'catalog'
        db_table = 'domain'
