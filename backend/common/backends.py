import os

from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """Authenticate with email (USERNAME_FIELD) for Django admin and sessions."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get("email")

        if username and "@" not in username:
            # Dev convenience: allow "admin" as shorthand for ADMIN_EMAIL.
            username = os.environ.get("ADMIN_EMAIL", "admin@localhost")

        if not username or not password:
            return None

        return super().authenticate(
            request, username=username, password=password, **kwargs
        )
