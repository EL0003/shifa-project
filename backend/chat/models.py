from django.db import models
from users.models import User
from doctors.models import DoctorProfile
from patients.models import PatientProfile


class ChatRoom(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('rejected', 'Rejected'),
    ]

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='chat_rooms')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='chat_rooms')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'patient')
        ordering = ['-created_at']

    def __str__(self):
        return f"Chat: {self.patient.full_name} ↔ Dr. {self.doctor.full_name} [{self.status}]"


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.email}: {self.content[:50]}"
