from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # patient, doctor, admin, assistant

    def __str__(self):
        return self.name

class User(models.Model):
    email = models.EmailField(max_length=60, unique=True)
    password_hash = models.CharField(max_length=128)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
