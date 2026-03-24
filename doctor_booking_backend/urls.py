from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import RegisterView, LoginView, LogoutView, MeView, RoleViewSet
from doctors.views import DoctorViewSet, ClinicViewSet, DoctorClinicViewSet, DoctorAvailabilityViewSet
from patients.views import PatientViewSet
from appointments.views import AppointmentViewSet, AppointmentStatusHistoryViewSet, ReviewViewSet
from medical_records.views import (MedicalRecordViewSet, ConsultationViewSet, DiagnosisViewSet,
    MedicationViewSet, PrescriptionViewSet, AttachmentViewSet)

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'clinics', ClinicViewSet)
router.register(r'doctor-clinics', DoctorClinicViewSet)
router.register(r'doctor-availability', DoctorAvailabilityViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'appointment-history', AppointmentStatusHistoryViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'diagnoses', DiagnosisViewSet)
router.register(r'medications', MedicationViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'attachments', AttachmentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/auth/register/', RegisterView.as_view()),
    path('api/auth/login/', LoginView.as_view()),
    path('api/auth/logout/', LogoutView.as_view()),
    path('api/auth/me/', MeView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),

    # API
    path('api/', include(router.urls)),
]
