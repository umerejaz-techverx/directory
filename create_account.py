#!/usr/bin/env python3

import sys, os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'directory.settings')
django.setup()

from django.contrib.auth.models import User

if User.objects.all().count() < 1:
    User.objects.create_superuser('testing', 'test@test.com', '1234')
