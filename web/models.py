import uuid

from django.contrib.auth.models import User
from django.db import models


class EmployeeDetails(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    contact = models.CharField(max_length=15, unique=True)
    salary = models.IntegerField(null=True, blank=True)
    manager = models.ForeignKey(User, related_name='manager', on_delete=models.CASCADE, null=True)
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
