from django.db import models
from users.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    full_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='doctors/images/', blank=True, null=True)
    license_number = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.full_name} - {self.specialization}"


class Clinic(models.Model):
    CLINIC_TYPES = [('private', 'Private'), ('hospital', 'Hospital'), ('center', 'Medical Center')]

    name = models.CharField(max_length=150)
    address_text = models.TextField()
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    opening_hours = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=20, choices=CLINIC_TYPES, default='private')

    def __str__(self):
        return f"{self.name} - {self.city}"


class DoctorClinic(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='clinics')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='doctors')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('doctor', 'clinic')

    def __str__(self):
        return f"Dr. {self.doctor.full_name} @ {self.clinic.name}"


class DoctorAvailability(models.Model):
    DAY_CHOICES = [
        ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday'),
    ]

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='availability')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('doctor', 'clinic', 'day_of_week')

    def __str__(self):
        return f"Dr. {self.doctor.full_name} - {self.day_of_week} ({self.start_time}-{self.end_time})"
