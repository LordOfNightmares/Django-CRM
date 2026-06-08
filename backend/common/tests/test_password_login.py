"""
Tests for email/password login (DEBUG-only dev endpoint).

Run with: pytest common/tests/test_password_login.py -v
"""

import pytest
from django.test import override_settings
from rest_framework import status

from common.models import Org, Profile, User


@pytest.mark.django_db
class TestPasswordLogin:
    url = "/api/auth/login/"

    @override_settings(DEBUG=True)
    def test_login_success(self, unauthenticated_client):
        User.objects.create_user(email="admin@test.com", password="secret123")
        response = unauthenticated_client.post(
            self.url,
            {"email": "admin@test.com", "password": "secret123"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data
        assert "refresh_token" in response.data
        assert response.data["user"]["email"] == "admin@test.com"

    @override_settings(DEBUG=True)
    def test_login_with_org_context(self, unauthenticated_client):
        user = User.objects.create_user(email="admin@test.com", password="secret123")
        org = Org.objects.create(name="Test Org")
        Profile.objects.create(user=user, org=org, role="ADMIN", is_active=True)

        response = unauthenticated_client.post(
            self.url,
            {"email": "admin@test.com", "password": "secret123"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_org"]["name"] == "Test Org"

    @override_settings(DEBUG=True)
    def test_login_invalid_password(self, unauthenticated_client):
        User.objects.create_user(email="admin@test.com", password="secret123")
        response = unauthenticated_client.post(
            self.url,
            {"email": "admin@test.com", "password": "wrong"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @override_settings(DEBUG=False)
    def test_login_disabled_when_debug_false(self, unauthenticated_client):
        User.objects.create_user(email="admin@test.com", password="secret123")
        response = unauthenticated_client.post(
            self.url,
            {"email": "admin@test.com", "password": "secret123"},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
