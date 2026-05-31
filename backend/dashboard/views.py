from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend

from doctors.models import DoctorProfile
from patients.models import PatientProfile
from appointments.models import Appointment, AppointmentMessage, Review
from notifications.models import Notification
from appointments.serializers import AppointmentSerializer, ReviewSerializer
from users.permissions import IsAdminOrDoctor, IsAuthenticated


def get_token_data(request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        backend = TokenBackend(algorithm='HS256', signing_key=settings.SECRET_KEY)
        return backend.decode(token, verify=True)
    except Exception:
        return None


class DoctorDashboardView(APIView):

    def get_permissions(self):
        return [IsAdminOrDoctor()]

    def get(self, request):
        token_data = get_token_data(request)
        if not token_data:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = token_data.get('user_id')
        role = token_data.get('role')

        if role == 'admin':
            doctor_id = request.query_params.get('doctor_id')
            if not doctor_id:
                return Response(
                    {'error': 'Admin must provide ?doctor_id=X'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                doctor = DoctorProfile.objects.get(id=doctor_id)
            except DoctorProfile.DoesNotExist:
                return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                doctor = DoctorProfile.objects.get(user_id=user_id)
            except DoctorProfile.DoesNotExist:
                return Response({'error': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.now().date()
        all_appointments = Appointment.objects.filter(doctor=doctor)

        today_appointments = all_appointments.filter(
            scheduled_datetime__date=today
        ).order_by('scheduled_datetime')

        pending_appointments = all_appointments.filter(
            status='pending'
        ).order_by('scheduled_datetime')

        total = all_appointments.count()
        completed = all_appointments.filter(status='completed').count()
        canceled = all_appointments.filter(status='canceled').count()
        rejected = all_appointments.filter(status='rejected').count()
        pending = all_appointments.filter(status='pending').count()
        confirmed = all_appointments.filter(status='confirmed').count()
        completion_rate = round((completed / total * 100), 1) if total > 0 else 0

        reviews = Review.objects.filter(appointment__doctor=doctor).order_by('-created_at')
        total_reviews = reviews.count()
        avg_rating = None
        if total_reviews > 0:
            avg = sum(
                r.rating_waiting + r.rating_hygiene + r.rating_attentiveness
                for r in reviews
            ) / (total_reviews * 3)
            avg_rating = round(avg, 2)

        unread_messages = AppointmentMessage.objects.filter(
            appointment__doctor=doctor,
            is_read=False
        ).exclude(sender_id=user_id).count()

        unread_notifications = Notification.objects.filter(
            user_id=user_id,
            is_read=False
        ).count()

        next_week = timezone.now() + timezone.timedelta(days=7)
        upcoming = all_appointments.filter(
            scheduled_datetime__gte=timezone.now(),
            scheduled_datetime__lte=next_week,
            status__in=['pending', 'confirmed']
        ).order_by('scheduled_datetime')

        return Response({
            'doctor': {
                'id': doctor.id,
                'full_name': doctor.full_name,
                'specialization': doctor.specialization,
                'is_verified': doctor.is_verified,
                'verification_status': doctor.verification_status,
                'consultation_fee': doctor.consultation_fee,
                'image': request.build_absolute_uri(doctor.image.url) if doctor.image else None,
            },
            'stats': {
                'total_appointments': total,
                'completed': completed,
                'canceled': canceled,
                'rejected': rejected,
                'pending': pending,
                'confirmed': confirmed,
                'completion_rate': completion_rate,
                'avg_rating': avg_rating,
                'total_reviews': total_reviews,
                'total_clinics': doctor.clinics.count(),
            },
            'today_appointments': AppointmentSerializer(today_appointments, many=True).data,
            'pending_appointments': AppointmentSerializer(pending_appointments, many=True).data,
            'upcoming_appointments': AppointmentSerializer(upcoming, many=True).data,
            'recent_reviews': ReviewSerializer(reviews[:5], many=True).data,
            'unread_messages': unread_messages,
            'unread_notifications': unread_notifications,
        })


class PatientDashboardView(APIView):

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request):
        token_data = get_token_data(request)
        if not token_data:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = token_data.get('user_id')

        try:
            patient = PatientProfile.objects.get(user_id=user_id)
        except PatientProfile.DoesNotExist:
            return Response({'error': 'Patient profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        all_appointments = Appointment.objects.filter(patient=patient)

        total = all_appointments.count()
        completed = all_appointments.filter(status='completed').count()
        canceled = all_appointments.filter(status='canceled').count()
        pending = all_appointments.filter(status='pending').count()
        confirmed = all_appointments.filter(status='confirmed').count()

        upcoming = all_appointments.filter(
            scheduled_datetime__gte=timezone.now(),
            status__in=['pending', 'confirmed']
        ).order_by('scheduled_datetime')

        past = all_appointments.filter(
            status__in=['completed', 'canceled', 'rejected']
        ).order_by('-scheduled_datetime')

        from medical_records.models import Prescription
        recent_prescriptions = Prescription.objects.filter(
            consultation__medical_record__patient=patient
        ).select_related(
            'medication', 'consultation__doctor'
        ).order_by('-consultation__consultation_date')[:5]

        prescriptions_data = [{
            'id': p.id,
            'medication_name': p.medication.name,
            'dosage': p.dosage,
            'duration_days': p.duration_days,
            'doctor_name': p.consultation.doctor.full_name,
            'date': p.consultation.consultation_date,
        } for p in recent_prescriptions]

        unread_notifications = Notification.objects.filter(
            user_id=user_id, is_read=False
        ).count()

        unread_messages = AppointmentMessage.objects.filter(
            appointment__patient=patient,
            is_read=False
        ).exclude(sender_id=user_id).count()

        return Response({
            'patient': {
                'id': patient.id,
                'full_name': patient.full_name,
                'phone_number': patient.phone_number,
                'email': patient.user.email,
                'date_of_birth': patient.date_of_birth,
                'gender': patient.gender,
            },
            'stats': {
                'total_appointments': total,
                'upcoming': upcoming.count(),
                'completed': completed,
                'canceled': canceled,
                'pending': pending,
                'confirmed': confirmed,
            },
            'upcoming_appointment': AppointmentSerializer(upcoming.first).data if upcoming.exists() else None,
            'upcoming_appointments': AppointmentSerializer(upcoming[:5], many=True).data,
            'past_appointments': AppointmentSerializer(past[:5], many=True).data,
            'recent_prescriptions': prescriptions_data,
            'unread_notifications': unread_notifications,
            'unread_notifications_count': unread_notifications,
            'unread_messages_count': unread_messages,
        })
