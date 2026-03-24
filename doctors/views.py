from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from users.permissions import IsAdminRole, IsAdminOrDoctor, IsAuthenticated
from .models import DoctorProfile, Clinic, DoctorClinic, DoctorAvailability
from .serializers import DoctorSerializer, ClinicSerializer, DoctorClinicSerializer, DoctorAvailabilitySerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['specialization', 'is_active']
    search_fields = ['full_name', 'specialization']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminRole()]  # only admin can create/update/delete doctors


class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city', 'type']
    search_fields = ['name', 'city', 'address_text']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminRole()]


class DoctorClinicViewSet(viewsets.ModelViewSet):
    queryset = DoctorClinic.objects.all()
    serializer_class = DoctorClinicSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'clinic']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminRole()]


class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'clinic', 'day_of_week']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminOrDoctor()]
