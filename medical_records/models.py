from django.db import models
from django.utils import timezone
from patients.models import PatientProfile
from doctors.models import DoctorProfile
from appointments.models import Appointment

class MedicalRecord(models.Model):
    patient = models.OneToOneField(PatientProfile, on_delete=models.CASCADE, related_name='medical_record')
    blood_type = models.CharField(max_length=5, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Medical Record - {self.patient.full_name}"


class Consultation(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='consultations')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='consultations')
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='consultation')
    consultation_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consultation #{self.id} - {self.doctor.full_name}"


class Diagnosis(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='diagnoses')
    description = models.TextField()

    def __str__(self):
        return f"Diagnosis for Consultation #{self.consultation.id}"


class Medication(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Prescription(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='prescriptions')
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    duration_days = models.IntegerField()

    def __str__(self):
        return f"{self.medication.name} - {self.dosage}"


class Attachment(models.Model):
    FILE_TYPES = [('image', 'Image'), ('pdf', 'PDF'), ('other', 'Other')]

    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='attachments')
    file_url = models.FileField(upload_to='consultations/attachments/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Attachment for Consultation #{self.consultation.id}"
