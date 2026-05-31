from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsAdminRole, IsAuthenticated
from .models import PatientProfile
from .serializers import PatientSerializer


def get_user_id(request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        backend = TokenBackend(algorithm='HS256', signing_key=settings.SECRET_KEY)
        data = backend.decode(token, verify=True)
        return data.get('user_id')
    except Exception:
        return None


class PatientViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['gender']
    search_fields = ['full_name', 'phone_number']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminRole()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        user_id = get_user_id(request)
        if not user_id:
            return Response(
                {'error': 'Invalid token.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            patient = PatientProfile.objects.get(user_id=user_id)
        except PatientProfile.DoesNotExist:
            return Response(
                {'error': 'Patient profile not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        if request.method == 'GET':
            return Response(self.get_serializer(patient).data)

        serializer = self.get_serializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
