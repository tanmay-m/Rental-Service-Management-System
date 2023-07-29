from django.db import models
import uuid

import enum
IMAGE_MAX_LEN = 500000

@enum.unique
class Role(str, enum.Enum):
    CUSTOMER = 'CUSTOMER'
    OWNER = 'OWNER'
    ADMIN = 'ADMIN'

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    email_id = models.EmailField(max_length=100, unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    role_type = models.CharField(max_length=100, blank=False, choices=Role.choices(), default=Role.CUSTOMER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateField(null=True, blank=True)

    def set_role_type(__self__, role_type):
        __self__.role_type = role_type
    
    def set_password(__self__, password):
        __self__.password = password
        
@enum.unique
class RentStatus(str, enum.Enum):
    PENDING = 'PENDING'
    AVAILABLE = 'AVAILABLE'
    BOOKED = 'BOOKED'
    REJECT='REJECT'

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

class Rent_Items(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE) # Owner
    car_model = models.CharField(max_length=100, blank=False) # Toyota
    image = models.CharField(max_length=IMAGE_MAX_LEN, blank=False) # base64 image | dumb way, but okay for now
    model_name = models.CharField(max_length=100, blank=False) # Corolla
    color = models.CharField(max_length=50, blank=False) # COLOR
    number_plate = models.CharField(max_length=50, blank=False, unique=True) # number plate
    created_at = models.DateTimeField(auto_now_add=True)
    rent_status = models.CharField(max_length=100, blank=False, choices=RentStatus.choices(), default=RentStatus.PENDING) # current status
    day_rent_rate = models.IntegerField(default=50,blank=False) # cost for renting out for one day
    latitude = models.CharField(max_length=100, blank=False) # latitude data for location
    longitude = models.CharField(max_length=100, blank=False) # longitude data for location

    def get_columns(__self__):
        return ["id", "user", "car_model", "image", "model_name", "color", "number_plate", "rent_status", "day_rent_rate", "latitude", "longitude"]
    
    def __repr__(self):
        return f'{self.id} {self.number_plate}, {self.day_rent_rate}'

class Orders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE) # Customer
    rent = models.ForeignKey(Rent_Items, on_delete=models.CASCADE)
    email_id = models.EmailField(max_length=100, unique=True, blank=False)
    payment_id = models.CharField(max_length=100, blank=False)
    amount = models.IntegerField(blank=False)
    from_date = models.DateField(blank=False)
    to_date = models.DateField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_columns(__self__):
        return ["id", "user", "rent", "email_id", "payment_id", "amount", "from_date", "to_date", "created_at"]