from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = "common"

    def ready(self):
        from django.contrib import admin

        from common.admin_auth import AdminEmailAuthenticationForm

        admin.site.login_form = AdminEmailAuthenticationForm
        import common.signals  # noqa: F401  # pylint: disable=unused-import
