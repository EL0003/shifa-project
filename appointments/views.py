from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsAdminRole, IsAdminOrDoctor, IsAuthenticated
from .models import Appointment, AppointmentStatusHistory, Review
from .serializers import AppointmentSerializer, AppointmentStatusHistorySerializer, ReviewSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'consultation_type', 'doctor', 'patient', 'clinic']
    search_fields = ['patient__full_name', 'doctor__full_name']

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]  # any logged in user can book
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminOrDoctor()]  # only admin/doctor can update/delete


class AppointmentStatusHistoryViewSet(viewsets.ModelViewSet):
    queryset = AppointmentStatusHistory.objects.all()
    serializer_class = AppointmentStatusHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['appointment']

    def get_permissions(self):
        return [IsAdminOrDoctor()]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['appointment']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]  # any logged in user can review
