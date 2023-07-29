from api.models import Users, Role, Orders
from api.models import Rent_Items, RentStatus
from pathlib import Path
import os

def get_booked_cars(user_id):
    rented_cars=[]
    user = Users.objects.get(id=user_id)
    orders = Orders.objects.filter(user=user).values(*Orders().get_columns())
    print("orders",orders)
    for order in orders:
        rent = list(Rent_Items.objects.filter(id=order["rent"]).values(*Rent_Items().get_columns()))[0]
        rented_cars.append({
            "order_id": order["id"],
            "rent_id": rent["id"],
            "from_date":order["from_date"],
            "to_date":order["to_date"],
            "car_model":rent["car_model"],
            "image":rent["image"],
            "model_name":rent["model_name"],
            "color":rent["color"],
            "number_plate":rent["number_plate"],
            "rent_status":rent["rent_status"],
            "day_rent_rate":rent["day_rent_rate"]
        })
        # rented_cars.append(dict(rent))
        print("Adding rented cars",rented_cars)

    return rented_cars

def get_pending_cars():
    return list(Rent_Items.objects.filter(rent_status=RentStatus.PENDING).values(*Rent_Items().get_columns()))

def get_rented_cars(user_id):
    res=list(Rent_Items.objects.filter(user_id=user_id).values(*Rent_Items().get_columns()))
    print("got list for user ", user_id, res)
    return res

def get_email(url, code):
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'email.txt')
    print("called the email", filename)
    with open(filename) as f:
        contents = f.read()
        contents = contents.replace("replacement_url", url)
        contents = contents.replace("replacement_code", code)
        return contents
