#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from catalog.models import Domain

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class DomainTests(APITestCase):

    def setUp(self):
        # Set up data for the whole TestCase
        self.manager_user = User.objects.create(username="manager")
        Token.objects.create(user=self.manager_user)
        self.simple_user = User.objects.create(username="user_1")
        Token.objects.create(user=self.simple_user)

        Domain.objects.create(name='https://www.google.com', is_private=False)
        Domain.objects.create(name='https://mail.google.com/', is_private=True)

    def test_get_domain_list_by_auth_user(self):
        """
        Ensure authenticated user gets list of all domains (public and private)
        """
        # count all domains
        domain_count = Domain.objects.count()

        token = Token.objects.get(user__username='user_1')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('api:domain-list')
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(content[u'count'], domain_count)

    def test_get_domain_list_by_guest_user(self):
        """
        Ensure guest user gets list of all public domains only
        """
        public_domain_count = Domain.objects.filter(is_private=False).count()

        url = reverse('api:domain-list')
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(content[u'count'], public_domain_count)

    def test_get_domain_detail_by_auth_user(self):
        """
        Ensure authenticated user gets all domains (public and private)
        """
        private_domain = Domain.objects.filter(is_private=True).first()
        public_domain = Domain.objects.filter(is_private=False).first()

        token = Token.objects.get(user__username='user_1')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('api:domain-detail', kwargs={'pk': private_domain.pk})
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(content[u'name'], private_domain.name)
        self.assertEqual(content[u'is_private'], private_domain.is_private)

        url = reverse('api:domain-detail', kwargs={'pk': public_domain.pk})
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(content[u'name'], public_domain.name)
        self.assertEqual(content[u'is_private'], public_domain.is_private)

    def test_get_domain_detail_by_guest_user(self):
        """
        Ensure guest user gets only public domains
        """
        private_domain = Domain.objects.filter(is_private=True).first()
        public_domain = Domain.objects.filter(is_private=False).first()

        url = reverse('api:domain-detail', kwargs={'pk': private_domain.pk})
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(content[u'detail'], u'Not found.')

        url = reverse('api:domain-detail', kwargs={'pk': public_domain.pk})
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(content[u'name'], public_domain.name)
        self.assertEqual(content[u'is_private'], public_domain.is_private)


    def test_create_domain(self):
        """
        Ensure we can create a new domain object.
        """
        domain_count = Domain.objects.count()

        token = Token.objects.get(user__username='manager')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('api:domain-list')
        domain_name = 'https://www.youtube.com/'
        data = {'name': domain_name, 'is_private': True}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Domain.objects.count(), domain_count + 1)

    def test_create_domain_validation(self):
        """
        Ensure we can create a new domain object.
        """
        domain_count = Domain.objects.count()

        token = Token.objects.get(user__username='manager')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('api:domain-list')

        # test domain name should start with 'https://'
        domain_name = 'http://www.youtube.com/'
        data = {'name': domain_name, 'is_private': True}
        response = self.client.post(url, data, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content['name'], ['Domain should start with "https://" '])

        # test domain should be accessible via internet
        domain_name = 'https://www.not_really_youtube.com/'
        data = {'name': domain_name, 'is_private': True}
        response = self.client.post(url, data, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content['name'], ['Name or service not known'])


    def test_create_domain_error(self):
        """
        Ensure we can create a new domain object.
        """
        domain_count = Domain.objects.count()

        token = Token.objects.get(user__username='user_1')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('api:domain-list')
        domain_name = 'https://www.youtube.com/'
        data = {'name': domain_name, 'is_private': True}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Domain.objects.count(), domain_count)
