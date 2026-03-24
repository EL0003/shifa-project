from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsAdminRole, IsAuthenticated
from .models import PatientProfile
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['gender']
    search_fields = ['full_name', 'phone_number']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminRole()]  # only admin can list all patients
        return [IsAuthenticated()]
