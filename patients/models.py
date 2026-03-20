from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
# Create your models here.


class Patient(models.Model):
    full_name = models.CharField(
        max_length=50 , null=True, blank=True)
    phone = models.CharField(
        max_length=15, unique=True,
        validators=[RegexValidator(regex=r'^\d{10,15}$', message='enter a valid phone number ')])
    email = models.EmailField(
        max_length=60, unique=True)  # login email
    birth_date = models.DateField(
        max_length=10 , null=True, blank=True)  # تاريخ الميلاد
    national_id = models.CharField(
        max_length=18, unique=True,
        validators=[RegexValidator(regex=r'^\d{18}$', message='National ID must contain 18 digits')])
    password = models.CharField(
        max_length=128)  # كلمة المرور المشفرة    

    def __str__(self):
        return self.full_name
