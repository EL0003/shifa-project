from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.backends import TokenBackend
from django.conf import settings


def get_role_from_request(request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        backend = TokenBackend(algorithm='HS256', signing_key=settings.SECRET_KEY)
        data = backend.decode(token, verify=True)
        return data.get('role')
    except Exception:
        return None


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return get_role_from_request(request) == 'admin'


class IsDoctorRole(BasePermission):
    def has_permission(self, request, view):
        return get_role_from_request(request) == 'doctor'


class IsPatientRole(BasePermission):
    def has_permission(self, request, view):
        return get_role_from_request(request) == 'patient'


class IsAdminOrDoctor(BasePermission):
    def has_permission(self, request, view):
        return get_role_from_request(request) in ['admin', 'doctor']


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return get_role_from_request(request) is not None
