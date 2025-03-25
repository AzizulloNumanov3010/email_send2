from django.urls import path
from .views import send_code, VerifyCode

urlpatterns = [
    path("send/", send_code.as_view(), name="send_code"),
    path("verify/", VerifyCode.as_view(), name="verify_code"),
]
