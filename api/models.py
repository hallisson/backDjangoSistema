# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save 
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings 
from django.utils.decorators import method_decorator
from django.db import transaction


# Intercepta requisição caso não esteja criado gera o token de acesso
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)


class Task(models.Model):
    hostname = models.CharField(max_length=256)
    ip_address = models.CharField(max_length=50)
    title= models.CharField(max_length=256)
    severity = models.CharField(max_length=30)
    cvss = models.CharField(max_length=30)
    publication_date = models.DateField(auto_now_add=False)
    status = models.BooleanField(default = True)

    def __str__(self):
        return "%s" % self.title