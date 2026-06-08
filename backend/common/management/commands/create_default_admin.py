import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create or update the default superuser (for Docker bootstrap)"

    def handle(self, *args, **options):
        email = os.environ.get("ADMIN_EMAIL", "admin@localhost").lower()
        password = os.environ.get("ADMIN_PASSWORD", "")

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    "WARNING: ADMIN_PASSWORD not set — using default 'admin'. "
                    "Change it immediately in production!"
                )
            )
            password = "admin"

        user = User.objects.filter(email=email).first()
        if user:
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Updated default admin user: {email}")
            )
            return

        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Created default superuser: {email}"))
