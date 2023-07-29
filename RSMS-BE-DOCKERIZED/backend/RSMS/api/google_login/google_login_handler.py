from .. import http_handler, token_handler
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from datetime import datetime, timedelta
import jwt
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
from api.models import Users, Role
import django.http as http
from django.shortcuts import render


@api_view(['POST'])
def google_login(request):
    data = json.loads(request.body)
    qr = Users(**data)
    query_res = Users.objects.filter(email_id=qr.email_id)
    if query_res.count() == 0:
        data['password'] = 'token'
        qr = Users(**data)
        qr.set_role_type('CUSTOMER')
        qr.save()
        token = token_handler.generate_jwt(qr.id)
        return http_handler.get_http_response({"message": "Success", "token": token}, status=200)
    else:
        token = token_handler.generate_jwt(query_res.get().id)
        return http_handler.get_http_response({"message": "Success", "token": token}, status=200)
