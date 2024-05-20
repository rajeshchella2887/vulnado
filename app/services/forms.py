from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class LaunchJobForm(forms.Form):
    INVENTORY_TYPE_CHOICES = []
    CREDENTIALS_TYPE_CHOICES = []

    template_id = forms.CharField(label="ID", disabled=True)
    inventory = forms.ChoiceField(label="Inventory", widget=forms.Select(), choices=INVENTORY_TYPE_CHOICES)
    credentials = forms.ChoiceField(
        label="Credentials", required=False, widget=forms.Select(), choices=CREDENTIALS_TYPE_CHOICES
    )
    parsed_extra_vars = forms.JSONField(required=False, widget=forms.HiddenInput())
    launch_url = forms.CharField(required=False, widget=forms.HiddenInput())
    provider = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        choice_data = kwargs.pop("choice_data", None)
        parsed_extra_vars = kwargs.pop("parsed_extra_vars", None)
        super().__init__(*args, **kwargs)

        if parsed_extra_vars:
            for i in range(len(parsed_extra_vars)):
                field_name = list(parsed_extra_vars)[i]
                self.fields[field_name] = forms.CharField(required=False)
                try:
                    self.initial[field_name] = list(parsed_extra_vars.values())[i]
                except KeyError:
                    self.initial[field_name] = ""

        if choice_data:
            for item in choice_data["inventory"]:
                self.INVENTORY_TYPE_CHOICES.append((item["inventory_id"], item["name"]))

            for item in choice_data["credentials"]:
                self.CREDENTIALS_TYPE_CHOICES.append((item["credentials_id"], item["name"]))

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Launch"))
        self.fields["inventory"].choices = self.INVENTORY_TYPE_CHOICES
        self.fields["credentials"].choices = self.CREDENTIALS_TYPE_CHOICES
