from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from users.views import (
    DoctorRegisterView,
    LoginView,
    LogoutView,
    MeView,
    PatientRegisterView,
    RegisterView,
    RoleViewSet,
)
from doctors.views import DoctorViewSet, ClinicViewSet, DoctorClinicViewSet, DoctorAvailabilityViewSet
from patients.views import PatientViewSet
from appointments.views import AppointmentMessageViewSet, AppointmentViewSet, AppointmentStatusHistoryViewSet, ReviewViewSet
from medical_records.views import (MedicalRecordViewSet, ConsultationViewSet, DiagnosisViewSet,
    MedicationViewSet, PrescriptionViewSet, AttachmentViewSet)
from notifications.views import NotificationViewSet
from chat.views import ChatRoomViewSet
from dashboard.views import DoctorDashboardView, PatientDashboardView

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'clinics', ClinicViewSet)
router.register(r'doctor-clinics', DoctorClinicViewSet)
router.register(r'doctor-availability', DoctorAvailabilityViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'appointment-history', AppointmentStatusHistoryViewSet)
router.register(r'appointment-messages', AppointmentMessageViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'diagnoses', DiagnosisViewSet)
router.register(r'medications', MedicationViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'attachments', AttachmentViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'chat', ChatRoomViewSet, basename='chat')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterView.as_view()),
    path('api/auth/register/patient/', PatientRegisterView.as_view()),
    path('api/auth/register/doctor/', DoctorRegisterView.as_view()),
    path('api/auth/login/', LoginView.as_view()),
    path('api/auth/logout/', LogoutView.as_view()),
    path('api/auth/me/', MeView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/', include(router.urls)),
    path('api/dashboard/doctor/', DoctorDashboardView.as_view()),
    path('api/dashboard/patient/', PatientDashboardView.as_view()),
    path('api/notifications/', include('notifications.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
