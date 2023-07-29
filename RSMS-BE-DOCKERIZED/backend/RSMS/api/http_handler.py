from django.shortcuts import render
from django.http import HttpResponse
import django.http as http
from api.models import Users, Rent_Items
import json
from rest_framework.decorators import api_view
from django.http import JsonResponse
import jwt
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core import serializers

def get_http_response(response, status):
    resp = HttpResponse(JsonResponse(response, safe=False), status=status, content_type="application/json")
    return resp
