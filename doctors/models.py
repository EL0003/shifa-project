from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
# Create your models here.


class Doctor(models.Model):
    full_name = models.CharField(
        max_length=100)
    specialty = models.CharField(
        max_length=100)
    phone = models.CharField(
        max_length=15, unique=True,
        validators=[RegexValidator(regex=r'^\d{10,15}$', message='enter a valid phone number ')])
    email = models.EmailField(
        max_length=60, unique=True , default='test@example.com')  # login email
    license_number = models.CharField(
        max_length=50, unique=True ,default='123456789')  # رقم الترخيص الطبي
    image = models.ImageField(
        upload_to='doctors/images/', blank=True, null=True)
    active = models.BooleanField(
        default=True)
    location = models.CharField(
        max_length=255, blank=True, null=True)
    password = models.CharField(
        max_length=128 , default=make_password('defaultpassword'))  # كلمة المرور المشفرة   

    def __str__(self):
        return f"Dr. {self.full_name} - {self.specialty}"
