from datetime import timezone
from email.policy import default
from django.db import models

# Create your models here.
from doctors.models import Doctor
from patients.models import Patient


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_time = models.DateTimeField(null=True, blank=True)# موعد الموعد (تاريخ + ساعة)
    

    status_choices = [
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('canceled', 'Canceled'),]
    status = models.CharField(
        max_length=10, choices=status_choices, default='pending')

    def __str__(self):
        return f"Appointment: {self.patient.full_name} with Dr. {self.doctor.full_name} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        # منع حجز نفس الطبيب في نفس الوقت
        unique_together = ('doctor', 'date_time')
