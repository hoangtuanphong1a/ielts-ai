from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@shared_task(autoretry_for=(OSError,), retry_backoff=True, max_retries=3)
def send_password_reset_email(user_id: int) -> None:
    """Gửi email đặt lại mật khẩu ở nền (T0.8, AUTH-05).

    Chạy nền để API trả lời ngay, không chờ máy chủ email. Lỗi mạng (OSError) thì thử lại tối đa 3 lần.
    Token tạo trong task: hết hạn 1 giờ tính từ lúc tạo (PASSWORD_RESET_TIMEOUT).
    """
    user = get_user_model().objects.filter(pk=user_id, is_active=True).first()
    if user is None or not user.email:
        return

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
    send_mail(
        subject="IELTS AI: đặt lại mật khẩu",
        message=(
            f"Chào {user.username},\n\n"
            f"Bấm vào link sau để đặt mật khẩu mới (hết hạn sau 1 giờ):\n{link}\n\n"
            "Nếu bạn không yêu cầu, hãy bỏ qua email này."
        ),
        from_email=None,
        recipient_list=[user.email],
    )
