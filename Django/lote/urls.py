# módulo do Django para criar urls
from django.urls import path,include

# pip install python-social-auth[django]

# Importe todas suas classes do views.py
from . views import *
from users import views as register
from django.core.exceptions import PermissionDenied

urlpatterns = [
]




