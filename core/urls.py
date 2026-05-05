from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, BusinessViewSet, SubscriptionViewSet, 
    ClientSubscriptionViewSet, VisitViewSet, BookingViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'businesses', BusinessViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'client-subscriptions', ClientSubscriptionViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
