from api.models import Rent_Items, Users, RentStatus
import json
from rest_framework.decorators import api_view
from .. import http_handler
from ..order.order_handler import filter_rent_items
from datetime import datetime
from django.db.models import Q
import random
from .coordinates import coordinates
import dateutil.parser 


@api_view(['POST'])
def create_rent_item(request):
    if not request.user_id:
        return http_handler.get_http_response({"message": "Invalid request, user_id not provided"}, status=400)
    data = json.loads(request.body)
    rent_item = Rent_Items(**data)
    userObj = Users(id=request.user_id)
    rent_item.user = userObj
    random_index = random.randint(0, len(coordinates) - 1)
    rent_item.latitude = coordinates[random_index]['latitude']
    rent_item.longitude = coordinates[random_index]['longitude']
    try:
        rent_item.full_clean()
    except Exception as e:
        print("exception in cleaning rent item data", e)
        return http_handler.get_http_response({"message" : "Invalid rent item data check, fields"}, 400)
    rent_item.save()
    return http_handler.get_http_response({"message": "Item Registered"}, status=200)


# TODO(Priti) change this to POST
@api_view(['POST'])
def fetch_rent_items(request, term, pageNo, pageSize):
    all_items = []
    query_result = []
    data = json.loads(request.body)
    from_date = dateutil.parser.parse(data["from_date"],dayfirst=True)
    to_date = dateutil.parser.parse(data["to_date"],dayfirst=True )
    print("From date",type(from_date))
    print("To date",type(to_date))   
    print("fetching rent items", RentStatus.AVAILABLE, term, pageNo, pageSize)
    skip = (pageNo - 1) * pageSize
    # TODO add a like query instead of direct match | Priti
    if term == "all_cars":
        print("all search")
        query_result = Rent_Items.objects.filter(Q(rent_status=RentStatus.AVAILABLE))[skip:pageSize].values(*Rent_Items().get_columns())
    else:
        query_result = Rent_Items.objects.filter(Q(rent_status=RentStatus.AVAILABLE) & (Q(car_model__icontains=term) | Q(model_name__icontains=term) | Q(color__icontains=term)))[skip:pageSize].values(*Rent_Items().get_columns())
    # TODO(Priti) extract date from the request body and pass here

    all_items = filter_rent_items(query_result,from_date,to_date)
    # print("ALL",all_items)
    return http_handler.get_http_response({"cars":all_items}, status=200)

@api_view(['GET'])

def approve_rent_item(request, rent_item_id, updateInt): #updateInt:1 -- approve 0 --- reject 
    if not request.user_id:
        return http_handler.get_http_response({"message": "Invalid request, user_id not provided"}, status=400)
    user = Users.objects.filter(id=request.user_id).values("role_type")[0]
    print("got user", user, type(user))
    if user["role_type"] != "ADMIN":
        return http_handler.get_http_response({"message": "User type is not admin"}, status=401)
    try:
        db_rent_item = Rent_Items.objects.get(id=rent_item_id)
        if updateInt==1:
            db_rent_item.rent_status = RentStatus.AVAILABLE
        elif updateInt==0:
            db_rent_item.rent_status = RentStatus.REJECT
        db_rent_item.save()
    except Exception as e:
        return http_handler.get_http_response({"message":"Error while updating rent item status"}, status=500)
    return http_handler.get_http_response({"message": "Item approved!"}, status=200)