from django.contrib.admin.forms import AdminAuthenticationForm


class AdminEmailAuthenticationForm(AdminAuthenticationForm):
    """Admin login form labelled for email-based users."""

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].label = "Email"
        self.fields["username"].widget.attrs.setdefault(
            "placeholder", "admin@localhost"
        )
