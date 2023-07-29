from django.shortcuts import render
import django.http as http
from api.models import Users, Role
import json
from rest_framework.decorators import api_view
from django.http import JsonResponse
import jwt
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .. import http_handler, token_handler
from . import user_helper
import random 

@api_view(['POST'])
def login(request):
    data = json.loads(request.body)
    request_user = Users(**data)
    query_res = Users.objects.filter(email_id=request_user.email_id)
    if query_res.count() != 1:
        return http_handler.get_http_response({"message": "Unauthorized"}, status=401)
    if request_user.password != query_res.get().password:
        return http_handler.get_http_response({"message": "Unauthorized"}, status=401)
    token = token_handler.generate_jwt(query_res.get().id)
    return http_handler.get_http_response({"message": "Success", "token": token}, status=200)

@api_view(['POST'])
def sign_up(request):
    data = json.loads(request.body)
    u = Users(**data)
    try:
        u.full_clean()
    except Exception as e:
        print("unable to login ", e)
        return http_handler.get_http_response({"message": "Unauthorized"}, status=401)
    u.save()
    token = token_handler.generate_jwt(u.id)
    return http_handler.get_http_response({"message": "Success", "token": token}, status=200)

@api_view(['POST'])
def forgot_password(request):
    data = json.loads(request.body)
    if "email_id" not in data:
        return http_handler.get_http_response({"message": "email id is missing"}, status=403)
    u = Users(**data)
    query_res = Users.objects.filter(email_id=u.email_id)
    if query_res.count() != 1:
        return http_handler.get_http_response({"message": "Unauthorized"}, status=401)
    digit_code = str(random.randrange(111111, 999999, 6))
    token_url = "http://localhost:3000/update?token=%s" % (token_handler.generate_jwt_obj({
        "user_id": str(query_res.get().id), 
        "ttl": str(datetime.now() + timedelta(minutes=1500000)),
        "verification_code": str(digit_code)
    }))

    content = user_helper.get_email(token_url, digit_code)
    message = Mail(
        from_email='isshaikh@iu.edu',
        to_emails=u.email_id,
        subject='Reset your password!',
        html_content=content
    )
    sg = SendGridAPIClient("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")
    response = sg.send(message)
    return http_handler.get_http_response({"message": "Welcome to forgot page!!!"}, status=200)

@api_view(['POST'])
def update_password(request):
    data = json.loads(request.body)
    if "token" not in data or "password" not in data or "code" not in data:
        return http_handler.get_http_response({"message": "invalid params"}, status=403)
    jwt_token = data["token"]
    password = data["password"]
    user_code = data["code"]
    try:
        jwt_res = token_handler.decode_jwt(jwt_token)
        token_time = (datetime.strptime(jwt_res["ttl"], '%Y-%m-%d %H:%M:%S.%f'))
        if token_time < datetime.now():
            return http_handler.get_http_response({"message": "link expired"}, status=403)
        user_id = jwt_res["user_id"]
        email_code = jwt_res["verification_code"]
        print("updating email id with code ", user_id, email_code)
        if email_code != user_code:
            print("want", email_code, "have ", user_code, email_code == user_code, type(email_code), type(user_code))
            return http_handler.get_http_response({"message": "verification code does not match"}, status=403)
        u = Users.objects.get(id=user_id)
        u.password = password
        u.save()
        return http_handler.get_http_response({"message": "Success"}, status=200)
    except Exception as e:
        print("exception while jwt verify", e)
        return http_handler.get_http_response({"message": "jwt verficiation failed"}, status=401)


@api_view(['GET'])
def fetch_user_details(request):
    if not request.user_id or request.user_id == "":
        return http_handler.get_http_response({"message": "user_id not present"}, status=400)
    user_id = request.user_id
    query_res = Users.objects.filter(id=user_id)
    if query_res.count() != 1:
        return http_handler.get_http_response({"message": "Unauthorized"}, status=401)
    user_obj = query_res.get()
    user_details_response = {"id": user_obj.id, "first_name": user_obj.first_name, "last_name": user_obj.last_name, "email_id": user_obj.email_id
    ,"role_type":user_obj.role_type}
    if user_obj.role_type == Role.CUSTOMER:
        # adding all the cars booked by this customer in the response
        user_details_response["cars_booked"] = user_helper.get_booked_cars(user_id)
    elif user_obj.role_type == Role.ADMIN:
        # adding all the cars that in pending status as of now
        user_details_response["cars_pending"] = user_helper.get_pending_cars()
    else:
        user_details_response["cars_rented"] = user_helper.get_rented_cars(user_id) 

    return http_handler.get_http_response(user_details_response, status=200)