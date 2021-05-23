import typing
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer as BaseModelSerializer
