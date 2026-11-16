import re
from datetime import timedelta
from unittest import mock

from django.contrib.auth.models import User
from django.core import mail
from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Profile, Role
from .permissions import IsAdminRole, IsTeacherOrAdmin


class ProfileSignalTests(TestCase):
    def test_new_user_gets_student_profile(self):
        user = User.objects.create_user("an", password="S3cure-pass!")
        self.assertEqual(user.profile.role, Role.STUDENT)
        self.assertEqual(user.profile.daily_minutes, 30)

    def test_superuser_gets_admin_role(self):
        admin = User.objects.create_superuser("boss", password="S3cure-pass!")
        self.assertEqual(admin.profile.role, Role.ADMIN)


class _AdminOnly(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        return Response({"ok": True})


class _StaffOnly(APIView):
    permission_classes = [IsTeacherOrAdmin]

    def get(self, request):
        return Response({"ok": True})


class RolePermissionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.student = User.objects.create_user("hs", password="S3cure-pass!")
        self.teacher = User.objects.create_user("gv", password="S3cure-pass!")
        Profile.objects.filter(user=self.teacher).update(role=Role.TEACHER)
        self.teacher.refresh_from_db()

    def call(self, view, user):
        req = self.factory.get("/x")
        force_authenticate(req, user=user)
        return view.as_view()(req).status_code

    def test_student_blocked_from_admin_and_staff(self):
        self.assertEqual(self.call(_AdminOnly, self.student), 403)
        self.assertEqual(self.call(_StaffOnly, self.student), 403)

    def test_teacher_allowed_staff_not_admin(self):
        self.assertEqual(self.call(_StaffOnly, self.teacher), 200)
        self.assertEqual(self.call(_AdminOnly, self.teacher), 403)


class MeApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hv", password="S3cure-pass!")
        self.client.force_authenticate(self.user)

    def test_me_includes_profile(self):
        data = self.client.get("/api/auth/me/").data
        self.assertEqual(data["profile"]["role"], "student")

    def test_patch_learning_goals(self):
        res = self.client.patch(
            "/api/auth/me/",
            {"profile": {"target_band": 7.0, "exam_date": "2027-03-15", "daily_minutes": 45}},
            format="json",
        )
        self.assertEqual(res.status_code, 200, res.data)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.target_band, 7.0)
        self.assertEqual(str(self.user.profile.exam_date), "2027-03-15")

    def test_cannot_promote_self_to_admin(self):
        self.client.patch("/api/auth/me/", {"profile": {"role": "admin"}}, format="json")
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.role, "student")

    def test_band_must_be_half_step(self):
        res = self.client.patch("/api/auth/me/", {"profile": {"target_band": 6.3}}, format="json")
        self.assertEqual(res.status_code, 400)


class PasswordChangeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hv2", password="Old-pass-123!")
        self.client.force_authenticate(self.user)

    def test_change_password(self):
        res = self.client.post("/api/auth/password/change/",
                               {"old_password": "Old-pass-123!", "new_password": "New-pass-456!"})
        self.assertEqual(res.status_code, 204, getattr(res, "data", None))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("New-pass-456!"))

    def test_wrong_old_password(self):
        res = self.client.post("/api/auth/password/change/",
                               {"old_password": "sai", "new_password": "New-pass-456!"})
        self.assertEqual(res.status_code, 400)
        self.assertIn("old_password", res.data)

    def test_weak_new_password_rejected(self):
        res = self.client.post("/api/auth/password/change/",
                               {"old_password": "Old-pass-123!", "new_password": "123"})
        self.assertEqual(res.status_code, 400)


class PasswordResetTests(APITestCase):
    def setUp(self):
        cache.clear()  # throttle dùng cache, tránh dính lượt giữa các test
        self.user = User.objects.create_user("hv3", email="hv3@example.com", password="Old-pass-123!")

    def _request_link(self, email="hv3@example.com"):
        return self.client.post("/api/auth/password/reset/", {"email": email})

    def _parse_link(self):
        body = mail.outbox[-1].body
        uid = re.search(r"uid=([^&\s]+)", body).group(1)
        token = re.search(r"token=([^&\s]+)", body).group(1)
        return uid, token

    def test_full_reset_flow(self):
        self.assertEqual(self._request_link().status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        uid, token = self._parse_link()
        res = self.client.post("/api/auth/password/reset/confirm/",
                               {"uid": uid, "token": token, "new_password": "Brand-new-789!"})
        self.assertEqual(res.status_code, 200, res.data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Brand-new-789!"))

    def test_token_single_use(self):
        self._request_link()
        uid, token = self._parse_link()
        body = {"uid": uid, "token": token, "new_password": "Brand-new-789!"}
        self.client.post("/api/auth/password/reset/confirm/", body)
        body["new_password"] = "Another-000!"
        self.assertEqual(self.client.post("/api/auth/password/reset/confirm/", body).status_code, 400)

    def test_unknown_email_same_response_no_mail(self):
        res = self._request_link("khongco@example.com")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_link_expires_after_one_hour(self):
        self._request_link()
        uid, token = self._parse_link()
        from django.contrib.auth.tokens import default_token_generator
        # Giả lập đồng hồ trôi qua 1 giờ 1 phút sau khi tạo link
        with mock.patch.object(default_token_generator, "_now",
                               return_value=default_token_generator._now() + timedelta(hours=1, minutes=1)):
            res = self.client.post("/api/auth/password/reset/confirm/",
                                   {"uid": uid, "token": token, "new_password": "Brand-new-789!"})
        self.assertEqual(res.status_code, 400)

    def test_throttled_after_five_requests(self):
        codes = [self._request_link("x@example.com").status_code for _ in range(6)]
        self.assertEqual(codes[:5], [200] * 5)
        self.assertEqual(codes[5], 429)
