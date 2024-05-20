from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from ntt_portal_library.contracts.choices import PROVIDER_TYPE_CHOICES
from providers.constants import (
    PROVIDER_ACCESS_TOKEN_FIELD,
    PROVIDER_PASSWORD_FIELD,
    PROVIDER_USE_ACCESS_TOKEN_FIELD,
    PROVIDER_USERNAME_FIELD,
)


class AddProviderForm(forms.Form):
    provider_name = forms.CharField(label="Provider Name", max_length=100)
    ip_address = forms.CharField(label="IP Address/FQDN")
    type = forms.ChoiceField(label="Type", choices=PROVIDER_TYPE_CHOICES)
    use_access_token = forms.BooleanField(label="Use Access Token", required=False)

    username = forms.CharField(label="Username", required=False)
    password = forms.CharField(label="Password", required=False, widget=forms.PasswordInput())
    access_token = forms.CharField(label="Access Token", required=False, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))
        self.fields["use_access_token"].widget.attrs["id"] = PROVIDER_USE_ACCESS_TOKEN_FIELD
        self.fields["access_token"].widget.attrs["id"] = PROVIDER_ACCESS_TOKEN_FIELD
        self.fields["username"].widget.attrs["id"] = PROVIDER_USERNAME_FIELD
        self.fields["password"].widget.attrs["id"] = PROVIDER_PASSWORD_FIELD

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        access_token = cleaned_data.get("access_token")
        use_access_token = cleaned_data.get("use_access_token")

        if use_access_token and ((not access_token) or (username or password)):
            raise ValidationError(
                "When using access token, access token must be supplied, " "username or password should not be present"
            )

        if not use_access_token and ((not username or not password) or access_token):
            raise ValidationError(
                "When using username & password, username and password must be supplied, "
                "access token should not be present"
            )


class UpdateProviderForm(forms.Form):
    # NOTE: we have to duplicate because we need to allow users to update whatever they want
    id = forms.CharField(label="ID (readonly)", disabled=True)

    provider_name = forms.CharField(label="Provider Name", max_length=100)
    ip_address = forms.CharField(label="IP Address")
    type = forms.ChoiceField(label="Type", choices=PROVIDER_TYPE_CHOICES)
    use_access_token = forms.BooleanField(label="Use Access Token", required=False)

    username = forms.CharField(label="Username", required=False)
    password = forms.CharField(label="Password", required=False, widget=forms.PasswordInput())
    access_token = forms.CharField(label="Access Token", required=False, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))
        self.fields["use_access_token"].widget.attrs["id"] = PROVIDER_USE_ACCESS_TOKEN_FIELD
        self.fields["access_token"].widget.attrs["id"] = PROVIDER_ACCESS_TOKEN_FIELD
        self.fields["username"].widget.attrs["id"] = PROVIDER_USERNAME_FIELD
        self.fields["password"].widget.attrs["id"] = PROVIDER_PASSWORD_FIELD
