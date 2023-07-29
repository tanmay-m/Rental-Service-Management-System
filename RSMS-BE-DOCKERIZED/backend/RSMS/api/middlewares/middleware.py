
import jwt
# import views
from datetime import datetime

class Authenticator:
    def authenticate(self, request):
        if "Authorization" not in request.headers or request.headers["Authorization"] == "":
            return
        token = request.headers["Authorization"]
        try:
            jwt_res = jwt.decode(token, key="software_engineering_sucks :(", algorithms=["HS256"])
            token_time = (datetime.strptime(jwt_res["ttl"], '%Y-%m-%d %H:%M:%S.%f'))
            request.is_authenticated = token_time >= datetime.now()
            request.user_id = jwt_res["user_id"]
            print("decoding api header for token ", request.user_id)
        except Exception as e:
            print("jwt verification failed", e)
            request.is_authenticated = False