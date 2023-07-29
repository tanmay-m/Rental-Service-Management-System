from django.shortcuts import render
from django.http import HttpResponse
import django.http as http
from api.models import Orders, Users, Rent_Items
import json
from rest_framework.decorators import api_view
from .. import http_handler
import dateutil.parser 
from datetime import datetime

@api_view(['POST'])
def create_order(request):
    if not request.user_id or request.user_id == "":
        return http_handler.get_http_response({"message" : "user_id not present in request"}, 401)
    data = json.loads(request.body)
    from_date = dateutil.parser.parse(data["from_date"], dayfirst=True)
    to_date = dateutil.parser.parse(data["to_date"], dayfirst=True)
    print(from_date.month, from_date.day, to_date.month, to_date.day)
    order_item = Orders(
        user=Users(id=request.user_id),
        rent=Rent_Items(id=data["rent"]),
        email_id=data["email_id"],
        payment_id=data["payment_id"],
        amount=data["amount"],
        from_date=from_date,
        to_date=to_date
    )
    try:
        order_item.full_clean()
    except Exception as e:
        print("except statement here", e)
        return http_handler.get_http_response({"message" : "Invalid order item data check fields"}, 400)
    order_item.save()
    return http_handler.get_http_response({"message": "Order created!"}, status=200)

# TODO(Priti) change function definition 
def filter_rent_items(items, from_date,to_date):
    print("filtering out ", len(items), from_date, to_date)
    filtered_res = []
    for item in items:
        # find if there exists an entry in orders table which have been booked and covers current time
        print("searching for rent item id", item["id"])
        matching_order = Orders.objects.filter(rent_id=item["id"])
        print("matching ordeer",matching_order)
        dayRate=item["day_rent_rate"]
        noOfDays = (to_date - from_date).days
        totalAmt = noOfDays * dayRate

        if len(matching_order) == 0:
            item_add={
                "id":item["id"],
                "user":item["user"],
                "car_model":item["car_model"],
                "image":item["image"],
                "model_name":item["model_name"],
                "color":item["color"],
                "number_plate":item["number_plate"],
                "rent_status":item["rent_status"],
                "day_rent_rate":item["day_rent_rate"],
                "latitude": item["latitude"],
                "longitude": item["longitude"],
                "totalAmt":totalAmt
            }
            filtered_res.append(item_add)
            continue

        if from_date=="" or to_date=="":
            totalAmt=dayRate
        else:
            # flag for checking if order item time covers the timeAt
            covered_by_booking = False
            for order in matching_order:
                print("date1 order",order.from_date.month, order.from_date.day, from_date.date().month, from_date.date().day)
                print("date2 order",order.to_date.month, order.to_date.day, to_date.date().month, to_date.date().day)
                # change logic and use from_date and to_date here
                print(order.from_date <= from_date.date() and from_date.date() <= order.to_date)
                print(order.from_date <= to_date.date() and to_date.date() <= order.to_date)
                if (order.from_date <= from_date.date() and from_date.date() <= order.to_date) or (order.from_date <= to_date.date() and to_date.date() <= order.to_date):
                    covered_by_booking = True
                    print("Rent item covered by order", order.id, "item", item["id"])
                    break
            if covered_by_booking:
                continue
            # current rent is not covered by any of the orders
           
            # calculate the number of days between the two dates
            print(f'adding item to result {item["id"]}', noOfDays, totalAmt)
            item_add={
                "id":item["id"],
                "user":item["user"],
                "car_model":item["car_model"],
                "image":item["image"],
                "model_name":item["model_name"],
                "color":item["color"],
                "number_plate":item["number_plate"],
                "rent_status":item["rent_status"],
                "day_rent_rate":item["day_rent_rate"],
                "latitude": item["latitude"],
                "longitude": item["longitude"],
                "totalAmt":totalAmt
            }
            filtered_res.append(item_add)
    
    return filtered_res
