from rest_framework import serializers
from .models import User, Business, Subscription, ClientSubscription, Visit, Booking
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'
        read_only_fields = ['owner']

class SubscriptionSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.name', read_only=True)
    class Meta:
        model = Subscription
        fields = '__all__'

class ClientSubscriptionSerializer(serializers.ModelSerializer):
    subscription_details = SubscriptionSerializer(source='subscription', read_only=True)
    days_left = serializers.SerializerMethodField()
    
    class Meta:
        model = ClientSubscription
        fields = '__all__'
        read_only_fields = ['start_date', 'end_date', 'remaining_visits']
        
    def get_days_left(self, obj):
        from django.utils import timezone
        delta = obj.end_date - timezone.now().date()
        return max(delta.days, 0)

class VisitSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.username', read_only=True)
    business_name = serializers.CharField(source='business.name', read_only=True)
    class Meta:
        model = Visit
        fields = '__all__'
        read_only_fields = ['date']

class BookingSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.username', read_only=True)
    business_name = serializers.CharField(source='business.name', read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['status', 'created_at']
