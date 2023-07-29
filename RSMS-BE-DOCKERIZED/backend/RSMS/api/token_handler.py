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

SECRET_KEY = "software_engineering_sucks :("

def generate_jwt(id):
    # generate access token
    # using a shit ass approach here, just return a new jwt token with an expiry
    return jwt.encode({"user_id": str(id), "ttl": str(datetime.now() + timedelta(minutes=1500000))}, SECRET_KEY)

def generate_jwt_obj(obj):
    # generate access token
    # using a shit ass approach here, just return a new jwt token with an expiry
    return jwt.encode(obj, SECRET_KEY)

def decode_jwt(jwt_token):
    jwt_res = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
    return jwt_res