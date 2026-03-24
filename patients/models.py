from django.db import models
from django.core.validators import RegexValidator
from users.models import User

class PatientProfile(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=15, unique=True,
        validators=[RegexValidator(regex=r'^\d{10,15}$', message='Enter a valid phone number')])
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.full_name
