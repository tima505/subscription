from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True, null=True)

class Business(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    
    def __str__(self):
        return self.name

class Subscription(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='subscriptions')
    name = models.CharField(max_length=255)
    duration_days = models.IntegerField()
    visit_limit = models.IntegerField(null=True, blank=True, help_text="Null for unlimited")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} - {self.business.name}"

class ClientSubscription(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_subscriptions')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    remaining_visits = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.client.username} - {self.subscription.name}"

class Visit(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits')
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.client.username} visited {self.business.name} at {self.date}"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('rejected', 'Отклонено'),
    )
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.client.username} booked {self.business.name} for {self.datetime} ({self.status})"
