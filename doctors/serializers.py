from rest_framework import serializers
from .models import DoctorProfile, Clinic, DoctorClinic, DoctorAvailability

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'

class DoctorClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorClinic
        fields = '__all__'

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'
