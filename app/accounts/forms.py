import random
import string

from accounts.constants import (
    BIND_DN_HELP_TEXT,
    BIND_PASSWORD_HELP_TEXT,
    CONNECTION_OPTIONS_HELP_TEXT,
    DENY_GROUP_HELP_TEXT,
    GROUP_SEARCH_HELP_TEXT,
    GROUP_TYPE_HELP_TEXT,
    GROUP_TYPE_PARAMS_HELP_TEXT,
    INITIAL_ORGANIZATION_MAP_JSON_TEMPLATE,
    ORGANIZATION_MAP_HELP_TEXT,
    REQUIRE_GROUP_HELP_TEXT,
    SERVER_URI_HELP_TEXT,
    START_TLS_HELP_TEXT,
    USER_ATTR_MAP_HELP_TEXT,
    USER_DN_TEMPLATE_HELP_TEXT,
    USER_FLAGS_BY_GROUP_HELP_TEXT,
    USER_SEARCH_HELP_TEXT,
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.forms import PasswordInput
from ntt_portal_library.contracts.choices import LDAP_GROUP_TYPE_CHOICES

from .apis import get_user_group


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )


class AddUpdateLDAPSettingsForm(forms.Form):
    # NOTE: id is used for update
    id = forms.IntegerField(label="ID", required=False, widget=forms.HiddenInput())

    name = forms.CharField(
        label="Name",
        max_length=100,
        help_text="Enter a name for this LDAP configuration",
    )

    # TODO: move to contracts, add as needed
    # TODO: need to pass in initial
    key = forms.ChoiceField(
        label="Type",
        choices=(("LDAP", "LDAP"),),
        disabled=True,
        widget=forms.HiddenInput(),
        initial="LDAP",
    )

    active = forms.BooleanField(
        label="Active",
        help_text="If true, ldap authentication will use this ldap config",
        initial=False,
    )

    # NOTE: need to get all the available users & groups from auth_service for the adding user
    # users = forms.MultipleChoiceField(label='Users', choices=(), required=False)
    # group = forms.MultipleChoiceField(label='Groups', choices=(), required=False)

    server_uri = forms.CharField(
        label="Server URI",
        required=True,
        help_text=SERVER_URI_HELP_TEXT,
        initial="ldap://localhost",
    )  # AUTH_LDAP_SERVER_URI
    bind_dn = forms.CharField(
        label="Bind DN", required=False, help_text=BIND_DN_HELP_TEXT, initial=""
    )  # AUTH_LDAP_BIND_DN
    bind_password = forms.CharField(
        label="Bind Password",
        widget=forms.PasswordInput,
        help_text=BIND_PASSWORD_HELP_TEXT,
    )  # AUTH_LDAP_BIND_PASSWORD
    start_tls = forms.BooleanField(
        label="Start TLS?", required=False, help_text=START_TLS_HELP_TEXT
    )  # AUTH_LDAP_START_TLS
    connection_options = forms.JSONField(
        label="Connection Options",
        required=False,
        help_text=CONNECTION_OPTIONS_HELP_TEXT,
        initial={},
    )  # AUTH_LDAP_CONNECTION_OPTIONS
    user_search = forms.JSONField(
        label="User Search",
        required=False,
        help_text=USER_SEARCH_HELP_TEXT,
        initial=None,
    )  # AUTH_LDAP_USER_SEARCH
    user_dn_template = forms.CharField(
        label="User DN Template",
        required=False,
        help_text=USER_DN_TEMPLATE_HELP_TEXT,
        initial="",
    )  # AUTH_LDAP_USER_DN_TEMPLATE
    user_attr_map = forms.JSONField(
        label="User Attribute Map",
        required=False,
        help_text=USER_ATTR_MAP_HELP_TEXT,
        initial={},
    )  # AUTH_LDAP_USER_ATTR_MAP
    #     # NOTE: we are not supporting multiple group search for now
    group_search = forms.JSONField(
        label="Group Search",
        required=False,
        help_text=GROUP_SEARCH_HELP_TEXT,
        initial=None,
    )  # AUTH_LDAP_GROUP_SEARCH
    group_type = forms.ChoiceField(
        label="Group Type",
        choices=LDAP_GROUP_TYPE_CHOICES,
        required=False,
        help_text=GROUP_TYPE_HELP_TEXT,
        initial=None,
    )  # AUTH_LDAP_GROUP_TYPE
    group_type_params = forms.JSONField(
        label="Group Type Params",
        required=False,
        help_text=GROUP_TYPE_PARAMS_HELP_TEXT,
        initial={},
    )  # AUTH_LDAP_GROUP_TYPE_PARAMS
    require_group = forms.CharField(
        label="Require Group",
        required=False,
        help_text=REQUIRE_GROUP_HELP_TEXT,
        initial="",
    )  # AUTH_LDAP_REQUIRE_GROUP
    deny_group = forms.CharField(
        label="Deny Group", required=False, help_text=DENY_GROUP_HELP_TEXT, initial=""
    )  # AUTH_LDAP_DENY_GROUP
    user_flags_by_group = forms.JSONField(
        label="User Flags by Group",
        required=False,
        help_text=USER_FLAGS_BY_GROUP_HELP_TEXT,
        initial={},
    )  # AUTH_LDAP_USER_FLAGS_BY_GROUP

    # NOTE: no need for org field, always default to user's org
    organization_map = forms.JSONField(
        label="Organization Map",
        required=False,
        help_text=ORGANIZATION_MAP_HELP_TEXT,
        initial=INITIAL_ORGANIZATION_MAP_JSON_TEMPLATE,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))


class UserOnboardingForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "required": "True"}),
        help_text="username should be unique",
        required=False,
    )
    password = forms.CharField(
        label="Password",
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control", "required": "True"}),
        help_text="Password must be at least 8 characters long",
        required=False,
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    phone = forms.CharField(
        label="Phone",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    groups = forms.MultipleChoiceField(
        label="Group",
        choices=[],
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        help_text="With the help of Shift + arrow, you can select multiple groups.",
    )

    IS_LDAP_CHOICES = [
        (False, "Local User"),
        (True, "LDAP User"),
    ]

    is_ldap = forms.ChoiceField(
        choices=IS_LDAP_CHOICES,
        required=False,
        initial=False,
        widget=forms.Select(attrs={"class": "form-control corner-right-dropdown"}),
    )

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop("session", None)
        super(UserOnboardingForm, self).__init__(*args, **kwargs)
        self.fields["groups"].choices = self.get_group_choices()
        self.fields["is_ldap"].initial = False

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-6"
        self.helper.field_class = "col-md-6"

        self.fields["is_ldap"].label = ""

        self.helper.layout = Layout(
            Div(
                Div(
                    "is_ldap",
                    css_class="col-md-6 text-center mt-2 corner-right-dropdown",
                ),
                css_class="row",
            ),
            Div(
                Div("username", css_class="col-md-6"),
                Div("password", css_class="col-md-6"),
                css_class="row",
            ),
            Div(
                Div(css_class="col-md-6"),
                Div("confirm_password", css_class="col-md-6 text-right"),
                css_class="row",
            ),
            Div(
                Div("first_name", css_class="col-md-6"),
                Div("last_name", css_class="col-md-6"),
                css_class="row",
            ),
            Div(
                Div("email", css_class="col-md-6"),
                Div("phone", css_class="col-md-6"),
                css_class="row",
            ),
            Div(
                Div("groups", css_class="col-md-6"),
                css_class="row",
            ),
            Div(
                Submit("submit", "Submit", css_class="btn btn-lg"),
                HTML('<a class="btn btn-lg" href="{% url "dashboards:users" %}">Cancel</a>'),
                css_class="col-md-12 text-center mt-2",
            ),
        )

        self.helper.layout.append(
            HTML(
                """
                    <style>
                        .corner-right-dropdown {
                            position: absolute;
                            top: 20px; /* Adjust the top margin as needed */
                            right: 22px; /* Adjust the right margin as needed */
                            width: 135px;
                        }
                    </style>
                    <script>
                        document.addEventListener("DOMContentLoaded", function () {
                            var userTypeField = document.getElementById("id_is_ldap");
                            var passwordField = document.getElementById("id_password");
                            var firstNameField = document.getElementById("id_first_name");
                            var lastNameField = document.getElementById("id_last_name");
                            var emailField = document.getElementById("id_email");
                            var phoneField = document.getElementById("id_phone");
                            var groupField = document.getElementById("id_groups");
                            var confirmField = document.getElementById("id_confirm_password");

                            function updateFieldAccessibility() {
                                var isLdapSelected = userTypeField.value === "True";

                                // Disable and make readonly the specified fields
                                passwordField.disabled = isLdapSelected;
                                passwordField.readOnly = isLdapSelected;

                                firstNameField.disabled = isLdapSelected;
                                firstNameField.readOnly = isLdapSelected;

                                lastNameField.disabled = isLdapSelected;
                                lastNameField.readOnly = isLdapSelected;

                                emailField.disabled = isLdapSelected;
                                emailField.readOnly = isLdapSelected;

                                phoneField.disabled = isLdapSelected;
                                phoneField.readOnly = isLdapSelected;
                                groupField.disabled = isLdapSelected;
                                groupField.querySelectorAll('option').forEach(option => option.disabled = isLdapSelected);

                                confirmField.disabled = isLdapSelected;
                                confirmField.readOnly = isLdapSelected;

                                // Clear the values of specific fields when switching from local to AD user
                                if (isLdapSelected) {
                                    passwordField.value = "";
                                    firstNameField.value = "";
                                    lastNameField.value = "";
                                    emailField.value = "";
                                    phoneField.value = "";
                                    confirmField.value = "";
                                }

                            }
                            updateFieldAccessibility();
                            userTypeField.addEventListener("change", updateFieldAccessibility);
                        });

                        $(document).ready(function () {
                            // Hide the confirm password label initially
                            $("label[for='id_confirm_password']").hide();
                            // Hide the confirm password field initially
                            $("#id_confirm_password").hide();

                            // Show confirm password label and field when clicking inside the password field
                            $("#id_password").focus(function () {
                                $("label[for='id_confirm_password']").show();
                                $("#id_confirm_password").show();
                            });
                        });

                    </script>
                """
            )
        )

    def get_group_choices(self):
        access = self.session.get("access")
        success, response = get_user_group(access)
        if success:
            groups_data = response.get("data", {}).get("groups", [])
            return [(groups["id"], groups["name"]) for groups in groups_data]
        return []

    def clean(self):
        cleaned_data = super().clean()
        is_ldap = cleaned_data.get("is_ldap")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if is_ldap == "True":
            cleaned_data["password"] = ""
            cleaned_data["confirm_password"] = ""
        else:
            if password and confirm_password and password != confirm_password:
                raise ValidationError("Password and Confirm Password must match.")

            try:
                validate_password(password)
            except DjangoValidationError as e:
                raise ValidationError(e.messages)

        return cleaned_data


class UserUpdateForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Username should be unique",
    )
    password = forms.CharField(
        label="Password",
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control", "render_value": True}),
        help_text="Password must be at least 8 characters long",
        required=False,
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    phone = forms.CharField(
        label="Phone",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    groups = forms.MultipleChoiceField(
        label="Group",
        choices=[],
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        help_text="With the help of Shift + arrow, you can select multiple groups.",
    )
    IS_LDAP_CHOICES = [
        (False, "LOCAL USER"),
        (True, "LDAP USER"),
    ]
    is_ldap = forms.ChoiceField(
        choices=IS_LDAP_CHOICES,
        required=False,
        initial=False,
        widget=forms.Select(attrs={"class": "form-control corner-right-dropdown"}),
    )

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop("session", None)
        self.access = kwargs.pop("access", None)
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        random_password = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        self.fields["password"].widget.attrs["value"] = random_password

        all_groups = self.get_all_group_choices()

        self.fields["groups"].choices = all_groups
        self.fields["is_ldap"].disabled = True
        self.fields["is_ldap"].label = ""

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-6"
        self.helper.field_class = "col-md-6"
        self.helper.layout = Layout(
            Div(
                Div(
                    "is_ldap",
                    css_class="col-md-6 text-center mt-2 corner-right-dropdown",
                ),
                css_class="row",
            ),
            Div(
                Div("username", css_class="col-md-6"),
                Div("password", css_class="col-md-6 position-relative"),
                css_class="row",
            ),
            Div(
                Div(css_class="col-md-6"),
                Div("confirm_password", css_class="col-md-6"),
                css_class="row",
            ),
            Div(
                Div("first_name", css_class="col-md-6"),
                Div("last_name", css_class="col-md-6"),
                css_class="row",
            ),
            Div(
                Div("email", css_class="col-md-6"),
                Div("phone", css_class="col-md-6"),
                css_class="row",
            ),
            Div(
                Div("groups", css_class="col-md-6"),
                css_class="row",
            ),
            Div(
                Submit("submit", "Update", css_class="btn btn-lg"),
                HTML('<a class="btn btn-lg" href="{% url "dashboards:users" %}">Cancel</a>'),
                css_class="col-md-12 text-center mt-2",
            ),
        )

        self.helper.layout.append(
            HTML(
                """

                <!-- Include jQuery -->
                <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>

                <style>

                    /* Apply blue background to read-only input fields */
                    input[readonly],
                    input[disabled] {
                        # background-color: #a6a6a6 !important;
                        color: #a7a7a7 !important;
                    }

                    /* Hide the default arrow in the is_ldap dropdown */
                    .corner-right-dropdown::-ms-expand {
                        display: none;
                    }

                    .corner-right-dropdown {
                        -webkit-appearance: none;
                        -moz-appearance: none;
                        appearance: none;
                        background-image: none;
                        position: absolute;
                            top: 20px; /* Adjust the top margin as needed */
                            right: 22px; /* Adjust the right margin as needed */
                            width: 175px;
                            text-align: center;
                            font-weight: bold;
                            padding-left: 45px; /* Adjust the left padding as needed */
                    }

                    .corner-right-edit {
                        -webkit-appearance: none;
                        -moz-appearance: none;
                        appearance: none;
                        background-image: none;
                        position: absolute;
                        top: 0px; /* Position from javascript after error or success */
                        right: 0px; /* Adjust the right margin as needed */
                    }

                    .position-relative {
                        position: absolute;  /* Add position relative */
                    }

                    .edit-btn {
                        position: absolute;
                        top: 140px;  /* Position for normal loading */
                        right: 58px;  /* Adjust the right position */
                        # transform: translateY(-50%);  /* Center vertically */
                    }

                    @media (max-width: 768px) {
                        .edit-btn {
                            position: absolute;
                            top: 298px;  /* Position for normal loading */
                            right: 58px;  /* Adjust the right position */
                        }
                    }

                </style>

                <script>
                    document.addEventListener("DOMContentLoaded", function () {
                        var userTypeField = document.getElementById("id_is_ldap");
                        var passwordField = document.getElementById("id_password");
                        var confirmField = document.getElementById("id_confirm_password");
                        var firstNameField = document.getElementById("id_first_name");
                        var lastNameField = document.getElementById("id_last_name");
                        var emailField = document.getElementById("id_email");
                        var phoneField = document.getElementById("id_phone");

                        userTypeField.style.backgroundColor = "#589eee"; // Blue background color
                        userTypeField.style.color = "#ffffff"; // White text color

                        function updateFieldAccessibility() {
                            var isLdapSelected = userTypeField.value === "True";

                            // Hide the default arrow in the is_ldap dropdown
                            userTypeField.style.backgroundImage = isLdapSelected ? "none" : "";

                            // Disable and make readonly the specified fields for AD user
                            passwordField.disabled = isLdapSelected;
                            passwordField.readOnly = isLdapSelected;

                            confirmField.disabled = isLdapSelected;
                            confirmField.readOnly = isLdapSelected;

                            // Additional fields to disable and make readonly for AD user
                            firstNameField.disabled = isLdapSelected;
                            firstNameField.readOnly = isLdapSelected;

                            lastNameField.disabled = isLdapSelected;
                            lastNameField.readOnly = isLdapSelected;

                            emailField.disabled = isLdapSelected;
                            emailField.readOnly = isLdapSelected;

                            phoneField.disabled = isLdapSelected;
                            phoneField.readOnly = isLdapSelected;
                        }

                        updateFieldAccessibility();

                        userTypeField.addEventListener("change", updateFieldAccessibility);
                    });

                    $(document).ready(function () {
                        // Hide the confirm password label initially
                        $("label[for='id_confirm_password']").hide();
                        // Hide the confirm password field initially
                        $("#id_confirm_password").hide();

                        // Show confirm password label and field when clicking inside the password field
                        $("#id_password").focus(function () {
                            $("label[for='id_confirm_password']").show();
                            $("#id_confirm_password").show();
                        });
                    });

                </script>
                """
            )
        )

    def get_all_group_choices(self):
        access = self.session.get("access")
        success, response = get_user_group(access)
        if success:
            groups_data = response.get("data", {}).get("groups", [])
            return [(group["id"], group["name"]) for group in groups_data]
        return []

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if not password:
            return cleaned_data

        if confirm_password and password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password must match.")

        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise forms.ValidationError(e.messages)

        return cleaned_data


# =====================================================================================================
#                                       Local User profile update
# =====================================================================================================


class LocalUserProfileUpdateForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=100,
        help_text="Username should be unique",
        widget=forms.TextInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    password = forms.CharField(
        label="Password",
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control", "render_value": True}),
        help_text="Password must be at least 8 characters long",
        required=False,
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    phone = forms.CharField(
        label="Phone",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "required": "True"}),
        required=False,
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop("session", None)
        super(LocalUserProfileUpdateForm, self).__init__(*args, **kwargs)
        random_password = "".join(random.choices(string.ascii_letters + string.digits, k=12))

        # Set the random password as the initial value for the password field
        self.fields["password"].widget.attrs["value"] = random_password
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-6"
        self.helper.field_class = "col-md-6"
        self.helper.layout = Layout(
            Div(
                Div("username", css_class="col-md-6"),
                Div("password", css_class="col-md-6"),
                css_class="row",
            ),
            Div(
                Div("first_name", css_class="col-md-6"),
                Div("last_name", css_class="col-md-6"),
                css_class="row",
            ),
            Div(
                Div("email", css_class="col-md-6"),
                Div("phone", css_class="col-md-6"),
                css_class="row",
            ),
            Div(
                Div("profile_picture", css_class="col-md-6"),
                css_class="row",
            ),
            Div(
                Submit("submit", "Update", css_class="btn btn-lg"),
                HTML('<a class="btn btn-lg" href="{% url "dashboards:index" %}">Cancel</a>'),
                css_class="col-md-12 text-center mt-2",
            ),
        )

        self.helper.layout.append(
            HTML(
                """

                <!-- Include jQuery -->
                <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>

                <style>

                    /* Apply blue background to read-only input fields */
                    input[readonly],
                    input[disabled] {
                        # background-color: #a6a6a6 !important;
                        color: #a7a7a7 !important;
                    }

                    /* Hide the default arrow in the is_ldap dropdown */
                    .corner-right-dropdown::-ms-expand {
                        display: none;
                    }

                    .corner-right-dropdown {
                        -webkit-appearance: none;
                        -moz-appearance: none;
                        appearance: none;
                        background-image: none;
                        position: absolute;
                            top: 20px; /* Adjust the top margin as needed */
                            right: 22px; /* Adjust the right margin as needed */
                            width: 175px;
                            text-align: center;
                            font-weight: bold;
                            padding-left: 45px; /* Adjust the left padding as needed */
                    }

                    .corner-right-edit {
                        -webkit-appearance: none;
                        -moz-appearance: none;
                        appearance: none;
                        background-image: none;
                        position: absolute;
                        top: 0px; /* Position from javascript after error or success */
                        right: 0px; /* Adjust the right margin as needed */
                    }

                    .position-relative {
                        position: absolute;  /* Add position relative */
                    }

                    .edit-btn {
                        position: absolute;
                        top: 140px;  /* Position for normal loading */
                        right: 58px;  /* Adjust the right position */
                        # transform: translateY(-50%);  /* Center vertically */
                    }

                    @media (max-width: 768px) {
                        .edit-btn {
                            position: absolute;
                            top: 298px;  /* Position for normal loading */
                            right: 58px;  /* Adjust the right position */
                        }
                    }
                </style>

                <script>
                    document.addEventListener("DOMContentLoaded", function () {

                        var usernameField = document.getElementById("id_username");
                        var passwordField = document.getElementById("id_password");
                        var firstNameField = document.getElementById("id_first_name");
                        var lastNameField = document.getElementById("id_last_name");
                        var emailField = document.getElementById("id_email");
                        var phoneField = document.getElementById("id_phone");

                        function updateFieldAccessibility() {

                            usernameField.readOnly = usernameField;
                            // Disable and make readonly the specified fields for AD user
                            passwordField.readOnly = passwordField;
                            // Additional fields to disable and make readonly for AD user
                            firstNameField.readOnly = firstNameField;
                            lastNameField.readOnly = lastNameField;
                            emailField.readOnly = emailField;
                            phoneField.readOnly = phoneField;
                        }

                        updateFieldAccessibility();
                    });

                </script>
                """
            )
        )
