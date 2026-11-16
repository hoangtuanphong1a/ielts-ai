from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import generics, permissions, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .tasks import send_password_reset_email
from .serializers import (
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()

# Schema chung cho response {"detail": "..."} (dùng cho Swagger)
DetailResponse = inline_serializer("Detail", {"detail": serializers.CharField()})


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(methods=["GET"], responses=UserSerializer)
@extend_schema(methods=["PATCH"], request=UserSerializer, responses=UserSerializer)
@api_view(["GET", "PATCH"])
def me(request):
    """GET: user + profile. PATCH: sửa email và mục tiêu học (AUTH-07, AUTH-09)."""
    if request.method == "PATCH":
        ser = UserSerializer(request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)
    return Response(UserSerializer(request.user).data)


@extend_schema(request=PasswordChangeSerializer, responses={204: OpenApiResponse(description="Đã đổi mật khẩu")})
@api_view(["POST"])
def password_change(request):
    """Đổi mật khẩu khi đã đăng nhập (AUTH-06)."""
    ser = PasswordChangeSerializer(data=request.data, context={"request": request})
    ser.is_valid(raise_exception=True)
    request.user.set_password(ser.validated_data["new_password"])
    request.user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequestView(APIView):
    """Gửi link đặt lại mật khẩu (AUTH-05).

    Luôn trả 200 dù email có tồn tại hay không, để không lộ email nào đã đăng ký.
    Giới hạn 5 lần/giờ mỗi IP (DEFAULT_THROTTLE_RATES["password_reset"]).
    """

    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "password_reset"

    @extend_schema(request=PasswordResetRequestSerializer, responses=DetailResponse)
    def post(self, request):
        ser = PasswordResetRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"]

        # Gửi email ở nền (Celery): API trả lời ngay, thời gian phản hồi
        # giống nhau dù email có tồn tại hay không.
        for user_id in User.objects.filter(email__iexact=email, is_active=True).values_list("pk", flat=True):
            send_password_reset_email.delay(user_id)

        return Response({"detail": "Nếu email có trong hệ thống, link đặt lại mật khẩu đã được gửi."})


@extend_schema(request=PasswordResetConfirmSerializer, responses={200: DetailResponse, 400: OpenApiResponse(description="Link sai hoặc hết hạn")})
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def password_reset_confirm(request):
    """Đặt mật khẩu mới từ link trong email (AUTH-05)."""
    ser = PasswordResetConfirmSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    invalid = Response({"detail": "Link không hợp lệ hoặc đã hết hạn."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pk = force_str(urlsafe_base64_decode(ser.validated_data["uid"]))
        user = User.objects.get(pk=pk, is_active=True)
    except (ValueError, TypeError, OverflowError, User.DoesNotExist):
        return invalid

    if not default_token_generator.check_token(user, ser.validated_data["token"]):
        return invalid

    try:
        validate_password(ser.validated_data["new_password"], user)
    except DjangoValidationError as e:
        return Response({"new_password": list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

    # Đổi mật khẩu làm token cũ mất hiệu lực (token gắn với hash mật khẩu)
    user.set_password(ser.validated_data["new_password"])
    user.save()
    return Response({"detail": "Đã đặt mật khẩu mới. Bạn có thể đăng nhập."})
