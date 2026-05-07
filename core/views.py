from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import User, Business, Subscription, ClientSubscription, Visit, Booking
from .serializers import UserSerializer, BusinessSerializer, SubscriptionSerializer, ClientSubscriptionSerializer, VisitSerializer, BookingSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'create_manager']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'])
    def clients(self, request):
        if request.user.role not in ['admin', 'manager']:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        clients = User.objects.filter(role='client')
        serializer = self.get_serializer(clients, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def create_manager(self, request):
        """Temporary endpoint to create manager user. Remove after use."""
        username = request.data.get('username', 'manager')
        password = request.data.get('password', 'manager123')

        # Delete existing manager if exists
        User.objects.filter(username=username).delete()

        # Create new manager
        user = User.objects.create_user(
            username=username,
            password=password,
            email='manager@example.com',
            role='manager'
        )
        return Response({
            'status': 'success',
            'username': user.username,
            'role': user.role
        })

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClientSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = ClientSubscription.objects.all()
    serializer_class = ClientSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return ClientSubscription.objects.filter(client=user)
        return ClientSubscription.objects.all().select_related('client', 'subscription')

    def create(self, request, *args, **kwargs):
        # Only admin/manager can assign subscriptions
        if request.user.role == 'client':
            return Response({'detail': 'Клиенты не могут назначать абонементы'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        subscription = serializer.validated_data['subscription']
        end_date = timezone.now().date() + timedelta(days=subscription.duration_days)
        serializer.save(
            end_date=end_date, 
            remaining_visits=subscription.visit_limit
        )

    @action(detail=True, methods=['post'])
    def deduct_visit(self, request, pk=None):
        if request.user.role not in ['admin', 'manager']:
            return Response({'detail': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        
        client_sub = self.get_object()
        
        # Check if subscription is still active
        if client_sub.end_date < timezone.now().date():
            return Response({'detail': 'Абонемент истёк'}, status=status.HTTP_400_BAD_REQUEST)
        
        if client_sub.remaining_visits is not None:
            if client_sub.remaining_visits <= 0:
                return Response({'detail': 'Посещения закончились'}, status=status.HTTP_400_BAD_REQUEST)
            client_sub.remaining_visits -= 1
            client_sub.save()
            
        # Record visit
        Visit.objects.create(
            client=client_sub.client,
            business=client_sub.subscription.business
        )
        return Response({'status': 'visit recorded', 'remaining': client_sub.remaining_visits})

class VisitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return Visit.objects.filter(client=user)
        return Visit.objects.all().select_related('client', 'business')

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return Booking.objects.filter(client=user).select_related('client', 'business')
        return Booking.objects.all().select_related('client', 'business')

    def create(self, request, *args, **kwargs):
        # Only admin/manager can create bookings
        if request.user.role == 'client':
            return Response({'detail': 'Клиенты не могут создавать записи'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if client has active subscription for this business
        client_id = request.data.get('client')
        business_id = request.data.get('business')
        
        if client_id and business_id:
            has_active_sub = ClientSubscription.objects.filter(
                client_id=client_id,
                subscription__business_id=business_id,
                end_date__gte=timezone.now().date(),
            ).filter(
                Q(remaining_visits__gt=0) | Q(remaining_visits__isnull=True)
            ).exists()
            
            if not has_active_sub:
                return Response(
                    {'detail': 'У клиента нет активного абонемента для этой компании. Сначала назначьте абонемент.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(status='pending')

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if request.user.role != 'client' or booking.client != request.user:
            return Response({'detail': 'Только клиент может подтвердить свою запись'}, status=status.HTTP_403_FORBIDDEN)
        if booking.status != 'pending':
            return Response({'detail': 'Запись уже обработана'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Find active subscription for this business
        active_sub = ClientSubscription.objects.filter(
            client=booking.client,
            subscription__business=booking.business,
            end_date__gte=timezone.now().date(),
        ).filter(
            Q(remaining_visits__gt=0) | Q(remaining_visits__isnull=True)
        ).first()
        
        if not active_sub:
            return Response(
                {'detail': 'У вас нет активного абонемента для этой компании. Обратитесь к администратору.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Deduct 1 visit
        if active_sub.remaining_visits is not None:
            active_sub.remaining_visits -= 1
            active_sub.save()
        
        # Record visit
        Visit.objects.create(client=booking.client, business=booking.business)
        
        booking.status = 'confirmed'
        booking.save()
        
        remaining = active_sub.remaining_visits
        msg = f'Запись подтверждена. Осталось посещений: {remaining if remaining is not None else "Безлимит"}'
        return Response({'status': 'confirmed', 'detail': msg})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        booking = self.get_object()
        if request.user.role != 'client' or booking.client != request.user:
            return Response({'detail': 'Только клиент может отклонить свою запись'}, status=status.HTTP_403_FORBIDDEN)
        if booking.status != 'pending':
            return Response({'detail': 'Запись уже обработана'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'rejected'
        booking.save()
        return Response({'status': 'rejected', 'detail': 'Запись отклонена'})
