# -*- coding: utf-8 -*-
"""Taskmanager tests.

This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from . import models


class TestProfileModel(TestCase):

    def test_profile_creation(self):
        User = get_user_model()
        user = User.objects.create(
            username="taskbuster", password="django-tutorial")
        self.assertIsInstance(user.profile, models.Profile)
        user.save()
        self.assertIsInstance(user.profile, models.Profile)


class TestProjectModel(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(
            username="taskbuster", password="django-tutorial")
        self.profile = self.user.profile

    def tearDown(self):
        self.user.delete()

    def test_validation_color(self):
        project = models.Project(
            user=self.profile,
            name="TaskManager"
        )
        self.assertTrue(project.color == "#fff")
        project.full_clean()

        for color in ["#1cA", "#1256aB"]:
            project.color = color
            project.full_clean()

        for color in ["1cA", "1256aB", "#1", "#12", "#1234",
                      "#12345", "#1234567"]:
            with self.assertRaises(
                    ValidationError,
                    msg="%s didn't raise a ValidationError" % color):
                project.color = color
                project.full_clean()
