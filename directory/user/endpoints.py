"""
Provide implementation of user endpoints.
"""
from django.urls import path

from user.views.password import UserPasswordSingle
from user.views.registration import UserRegistrationSingle

user_endpoints = [
    path('password/', UserPasswordSingle.as_view()),
    path('registration/', UserRegistrationSingle.as_view()),
]
