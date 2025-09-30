#!/usr/bin/env python3
"""URL routes for listings API."""

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PaymentViewSet, ListingViewSet, BookingViewSet

router = DefaultRouter()
router.register("listings", ListingViewSet, basename="listings")
router.register("bookings", BookingViewSet, basename="bookings")
router.register("payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("", include(router.urls)),
]
