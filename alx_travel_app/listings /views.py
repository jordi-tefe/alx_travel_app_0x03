#!/usr/bin/env python3
"""API views for Listing and Booking."""

from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
import requests
import uuid
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment, Booking
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for handling Chapa payments."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=True, methods=["post"])
    def initiate(self, request, pk=None):
        """Initiate payment for a booking using Chapa API."""
        booking = Booking.objects.get(pk=pk)
        amount = booking.total_price
        tx_ref = str(uuid.uuid4())

        payload = {
            "amount": str(amount),
            "currency": "ETB",
            "email": booking.user.email,
            "first_name": booking.user.first_name,
            "last_name": booking.user.last_name,
            "tx_ref": tx_ref,
            "callback_url": "http://localhost:8000/api/payments/verify/",
        }

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"{settings.CHAPA_BASE_URL}/transaction/initialize",
            json=payload,
            headers=headers,
        )

        if response.status_code == 200:
            data = response.json()["data"]
            payment = Payment.objects.create(
                booking=booking, amount=amount, transaction_id=tx_ref, status="Pending"
            )
            return Response({"checkout_url": data["checkout_url"], "payment_id": payment.id})
        return Response(response.json(), status=response.status_code)

    @action(detail=False, methods=["get"])
    def verify(self, request):
        """Verify a payment with Chapa API."""
        tx_ref = request.query_params.get("tx_ref")
        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}

        response = requests.get(
            f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}", headers=headers
        )

        if response.status_code == 200:
            data = response.json()["data"]
            try:
                payment = Payment.objects.get(transaction_id=tx_ref)
                if data["status"] == "success":
                    payment.status = "Completed"
                    payment.save()
                    return Response({"message": "Payment successful!"})
                else:
                    payment.status = "Failed"
                    payment.save()
                    return Response({"message": "Payment failed."}, status=400)
            except Payment.DoesNotExist:
                return Response({"error": "Transaction not found"}, status=404)
        return Response(response.json(), status=response.status_code)


class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing travel listings."""
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user bookings."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
