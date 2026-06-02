from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend
from users.permissions import IsAuthenticated, IsDoctorRole, get_role_from_request
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer
from doctors.models import DoctorProfile
from patients.models import PatientProfile


def get_user_id_from_request(request):
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


class ChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer

    def get_permissions(self):
        if self.action in ['accept', 'reject']:
            return [IsAuthenticated(), IsDoctorRole()]
        return [IsAuthenticated()]

    def get_queryset(self):
        role = get_role_from_request(self.request)
        user_id = get_user_id_from_request(self.request)
        if role == 'doctor':
            return ChatRoom.objects.filter(doctor__user_id=user_id)
        if role == 'patient':
            return ChatRoom.objects.filter(patient__user_id=user_id)
        if role == 'admin':
            return ChatRoom.objects.all()
        return ChatRoom.objects.none()

    def perform_create(self, serializer):
        role = get_role_from_request(self.request)
        user_id = get_user_id_from_request(self.request)
        is_doctor = role == 'doctor'

        if role == 'doctor':
            doctor = DoctorProfile.objects.get(user_id=user_id)
            serializer.save(doctor=doctor, status='active')
        elif role == 'patient':
            patient = PatientProfile.objects.get(user_id=user_id)
            serializer.save(patient=patient, status='pending')
        else:
            serializer.save(status='pending')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        room = self.get_object()
        role = get_role_from_request(request)
        if role != 'doctor':
            return Response({'error': 'Only doctors can accept requests.'},
                            status=status.HTTP_403_FORBIDDEN)
        if room.status != 'pending':
            return Response({'error': f'Room is already {room.status}.'},
                            status=status.HTTP_400_BAD_REQUEST)
        room.status = 'active'
        room.save(update_fields=['status'])
        return Response(ChatRoomSerializer(room, context={'request': request}).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        room = self.get_object()
        role = get_role_from_request(request)
        if role != 'doctor':
            return Response({'error': 'Only doctors can reject requests.'},
                            status=status.HTTP_403_FORBIDDEN)
        if room.status != 'pending':
            return Response({'error': f'Room is already {room.status}.'},
                            status=status.HTTP_400_BAD_REQUEST)
        room.status = 'rejected'
        room.save(update_fields=['status'])
        return Response(ChatRoomSerializer(room, context={'request': request}).data)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        room = self.get_object()
        msgs = room.messages.all()
        serializer = ChatMessageSerializer(msgs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        room = self.get_object()
        user_id = get_user_id_from_request(request)
        room.messages.filter(is_read=False).exclude(sender_id=user_id).update(is_read=True)
        return Response({'message': 'Messages marked as read.'})
