from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsAdminRole, IsAdminOrDoctor, IsAuthenticated
from .models import MedicalRecord, Consultation, Diagnosis, Medication, Prescription, Attachment
from .serializers import (MedicalRecordSerializer, ConsultationSerializer,
    DiagnosisSerializer, MedicationSerializer, PrescriptionSerializer, AttachmentSerializer)


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient']

    def get_permissions(self):
        return [IsAdminOrDoctor()]


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'medical_record']

    def get_permissions(self):
        return [IsAdminOrDoctor()]


class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['consultation']

    def get_permissions(self):
        return [IsAdminOrDoctor()]


class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminOrDoctor()]


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['consultation', 'medication']

    def get_permissions(self):
        return [IsAdminOrDoctor()]


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['consultation']

    def get_permissions(self):
        return [IsAdminOrDoctor()]
