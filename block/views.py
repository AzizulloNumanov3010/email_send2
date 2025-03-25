import random
import smtplib
import ssl
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
import string

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_ADDRESS = "webdastur02@gmail.com"
EMAIL_PASSWORD = ""

class send_code(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email manzilini kiriting!"}, status=status.HTTP_400_BAD_REQUEST)

        verification_code = str(random.randint(100000, 999999))


        user, created = User.objects.get_or_create(email=email)
        user.verification_code = verification_code
        user.is_verified = False
        user.save()


        subject = "Tasdiqlash Kodingiz"
        body = f"Sizning tasdiqlash kodingiz: {verification_code}"
        message_text = f"Subject: {subject}\n\n{body}"
        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, email, message_text)
        except Exception as e:
            return Response({"error": f"Email yuborishda xatolik: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "✅ Tasdiqlash kodi emailingizga yuborildi."}, status=status.HTTP_201_CREATED)


def generate_fake_gmail():
    letters = string.ascii_lowercase
    random_part = ''.join(random.choices(letters + string.digits, k=8))
    email = f"{random_part}@gmail.com"

    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = ''.join(random.choices(characters, k=12))

    return email, password


class VerifyCode(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            user = User.objects.get(email=email)
            if user.verification_code == code:
                user.is_verified = True
                if not user.genemail:
                    user.genemail = generate_fake_gmail()

                    # 🔴 Yangi tasdiqlash kodini yaratamiz va saqlaymiz
                new_code = generate_fake_gmail()
                user.gen_code = new_code
                user.save()

                return Response({
                    "message": "✅ Tasdiqlash muvaffaqiyatli amalga oshdi!",
                    "genemail": user.genemail,  # 🔴 Yangi generatsiya qilingan email
                    "gen_code": user.gen_code  # 🔴 Yangi kod
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "❌ Noto‘g‘ri kod, qayta urinib ko‘ring."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "❌ Bunday email ro‘yxatda yo‘q!"}, status=status.HTTP_404_NOT_FOUND)

# edul vpxf cqas fpdk