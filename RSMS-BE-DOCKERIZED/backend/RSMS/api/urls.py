from django.urls import path

from .order import order_handler

from .rent_item import rent_item_handler

from .user import user_handler
from .google_login import google_login_handler

#URLConf
urlpatterns = [
    path("login/", user_handler.login),
    path("signup/", user_handler.sign_up),
    path("forgot/", user_handler.forgot_password),
    path("updatepassword/", user_handler.update_password),
    path("fetchuserdetails/", user_handler.fetch_user_details),
    path("createrentitem/", rent_item_handler.create_rent_item),
    path("fetchrentitems/<str:term>/<int:pageNo>/<int:pageSize>/", rent_item_handler.fetch_rent_items),
    path("createorder/", order_handler.create_order),
    path("googlelogin/", google_login_handler.google_login),
    path("approverentitem/<str:rent_item_id>/<int:updateInt>/", rent_item_handler.approve_rent_item)
]
