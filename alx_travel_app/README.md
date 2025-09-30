# ALX Travel App 0x02 – Chapa Payment Integration

## Overview
This project integrates the **Chapa API** into a Django travel booking app, enabling secure payment initiation, verification, and status tracking.

## Features
- Initiate payments with Chapa API
- Store and track payments with a `Payment` model
- Verify payments and update booking/payment status
- REST API endpoints for `initiate` and `verify`
- Uses environment variables for API keys
- Supports Celery email notifications after successful payment

## API Endpoints
- `POST /api/payments/{booking_id}/initiate/` → Start payment
- `GET /api/payments/verify/?tx_ref={tx_ref}` → Verify payment

## Setup
1. Add your Chapa API key in `.env`:
