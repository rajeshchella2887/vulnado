import json
from typing import List, Tuple

from accounts.forms import (
    AddUpdateLDAPSettingsForm,
    LocalUserProfileUpdateForm,
    LoginForm,
    UserOnboardingForm,
    UserUpdateForm,
)
from django.contrib import messages
from django.contrib.auth import views as django_auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from ntt_portal_library.contracts.api_contracts.accounts.add_ldap_settings_contract import AddLDAPSettingsDataDomain
from ntt_portal_library.contracts.api_contracts.accounts.create_ldap_user_contract import CreateLdapUserDataDomain
from ntt_portal_library.contracts.api_contracts.accounts.create_user_contract import CreateUserDataDomain
from ntt_portal_library.contracts.api_contracts.accounts.delete_ldap_settings_contract import (
    DeleteLDAPSettingsDataDomain,
)
from ntt_portal_library.contracts.api_contracts.accounts.delete_user_contract import DeleteUserDataDomain
from ntt_portal_library.contracts.api_contracts.accounts.get_ldap_settings_for_update_contract import (
    GetLDAPSettingsForUpdateDataDomain,
)
from ntt_portal_library.contracts.api_contracts.accounts.update_ad_user_contract import UpdateAdUserDataDomain
from ntt_portal_library.contracts.api_contracts.accounts.update_user_contract import UpdateUserDataDomain
from ntt_portal_library.contracts.api_contracts.accounts.update_user_without_password_contract import (
    UpdateUserWithoutPasswordDataDomain,
)
from ntt_portal_library.contracts.api_contracts.accounts.user_logout_contract import UserLogoutDataDomain
from ntt_portal_library.domains.accounts import GetUserProfileDataDomain
from utils.mixins.view_mixins import NTTDefaultLoginRequiredMixin, SegmentBreadCrumbEnabledMixin

from .apis import (
    add_ldap_settings,
    add_user,
    create_ldap_user,
    delete_ldap_settings,
    delete_user,
    delete_users,
    get_ldap_settings_for_update,
    get_user_for_update,
    getting_user_profile,
    update_ad_user,
    update_ldap_settings,
    update_user,
    update_user_without_password,
    updating_user_profile,
    user_logout,
)
from .constants import NESTED_LDAP_FIELDS


# Create your views here.
class LoginView(django_auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "accounts/auth-signin-img-side.html"
    authentication_form = LoginForm
    next_page = "dashboards:compliance-management"  # TODO: change it back to index


class LogoutView(django_auth_views.LogoutView):
    next_page = "accounts:login"

    @classmethod
    def logout(cls, sender, user, request, **kwargs):
        """
        NOTE: this method invalidates the token kept at auth service
        """

        # NOTE: we need to extract manually because session might be polluted with other stuff
        #       let fail naturally if items are not present
        refresh = request.session.get("refresh")

        # NOTE: we do not need to do anything with the response,
        #       django Logout view will flush our session
        user_logout(UserLogoutDataDomain(refresh=refresh))


user_logged_out.connect(LogoutView.logout, sender=LogoutView)


class LDAPSettings(NTTDefaultLoginRequiredMixin, TemplateView):
    template_name = "accounts/auth-settings/ldap/settings.html"


class AddLDAPSettingsView(NTTDefaultLoginRequiredMixin, View, SegmentBreadCrumbEnabledMixin):
    form_class = AddUpdateLDAPSettingsForm
    template_name = "accounts/auth-settings/ldap/add-settings.html"

    @property
    def segment(self) -> str:
        return "Add Provider"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("authentication", reverse("dashboards:authentication")),
            ("add ldap settings", reverse("accounts:add_ldap_settings")),
        ]

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, self.get_context_data(form=form))

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            return self.handle_form_valid(request, form)

        return render(request, self.template_name, self.get_context_data(form=form))

    def handle_form_valid(self, request, form):
        nested_ldap_data_domain = {key: value for key, value in form.cleaned_data.items() if key in NESTED_LDAP_FIELDS}
        compliant_ldap_data_domain = {
            "name": form.cleaned_data["name"],
            "key": form.cleaned_data["key"],
            "value": nested_ldap_data_domain,
            "active": form.cleaned_data["active"],
        }

        success, response = add_ldap_settings(request, AddLDAPSettingsDataDomain(**compliant_ldap_data_domain))

        if success:
            return redirect(reverse("dashboards:authentication"))
        else:
            return render(
                request,
                self.template_name,
                self.get_context_data(form=form, errors=response.errors),
            )


class UpdateLDAPSettingsView(NTTDefaultLoginRequiredMixin, View, SegmentBreadCrumbEnabledMixin):
    form_class = AddUpdateLDAPSettingsForm
    template_name = "accounts/auth-settings/ldap/add-settings.html"

    ldap_settings_pk: str = None

    @property
    def segment(self) -> str:
        return "Update LDAP Settings"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("providers", reverse("dashboards:authentication")),
            (
                "update ldap settings",
                reverse(
                    "accounts:update_ldap_settings",
                    kwargs={"pk": self.ldap_settings_pk},
                ),
            ),
        ]

    def get(self, request, pk):
        # NOTE: used for path_to_current_view to pass pk to the frontend
        self.ldap_settings_pk = pk

        success, response = get_ldap_settings_for_update(request, GetLDAPSettingsForUpdateDataDomain(id=int(pk)))

        # NOTE: flatten nested data
        initial_data = {
            "id": response.data.id,
            "name": response.data.name,
            "key": response.data.key,
            **response.data.value.to_dict(),
        }

        if success:
            form = self.form_class(initial=initial_data)
            return render(request, self.template_name, self.get_context_data(form=form))
        else:
            return redirect(reverse("dashboards:authentication"))

    def post(self, request, pk):
        self.ldap_settings_pk = pk

        form = self.form_class(data=request.POST, initial={"id": pk})
        if form.is_valid():
            return self.handle_form_valid(request, form)

        return render(request, self.template_name, self.get_context_data(form=form))

    def handle_form_valid(self, request, form):
        nested_ldap_data_domain = {key: value for key, value in form.cleaned_data.items() if key in NESTED_LDAP_FIELDS}
        compliant_ldap_data_domain = {
            "name": form.cleaned_data["name"],
            "key": form.cleaned_data["key"],
            "value": nested_ldap_data_domain,
            "active": form.cleaned_data["active"],
        }

        identifier_ldap_data_domain = GetLDAPSettingsForUpdateDataDomain(id=int(self.ldap_settings_pk))
        success, response = update_ldap_settings(
            request,
            identifier_ldap_data_domain,
            AddLDAPSettingsDataDomain(**compliant_ldap_data_domain),
        )
        if success:
            return redirect(reverse("dashboards:authentication"))
        else:
            return render(
                request,
                self.template_name,
                self.get_context_data(form=form, errors=response.errors),
            )


class DeleteLDAPSettingsView(NTTDefaultLoginRequiredMixin, View):
    def delete(self, request, pk):
        success, response = delete_ldap_settings(request, DeleteLDAPSettingsDataDomain(id=pk))

        if success:
            return HttpResponse(f"LDAP Settings {pk} deleted")

        return HttpResponseBadRequest()


class UserOnboardingView(FormView, NTTDefaultLoginRequiredMixin, SegmentBreadCrumbEnabledMixin):
    template_name = "accounts/user_onboarding.html"
    form_class = UserOnboardingForm
    success_url = "/accounts/create-user/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["session"] = self.request.session
        return kwargs

    @property
    def segment(self) -> str:
        return "User Onboarding"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("Users", reverse("dashboards:users")),
            ("User Onboarding", reverse("accounts:create_user")),
        ]

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        if form.cleaned_data["is_ldap"] == "True":
            data = CreateLdapUserDataDomain(username=username)
            success, response = create_ldap_user(self.request, data)
            response_data = response
            if response_data.get("type") == "server_error":
                for error in response_data.get("errors", []):
                    error_detail = error.get("detail")
                    if error_detail:
                        form.add_error(None, error_detail)
                return self.form_invalid(form)
            elif response_data.get("success"):
                user_data = response_data.get("data", {})
                for field_name, field_value in user_data.items():
                    if field_name in form.fields:
                        form.fields[field_name].initial = field_value
                messages.success(self.request, f"Username {username} created successfully!")
                return redirect(self.success_url)
            else:
                return redirect(self.success_url)

        else:
            cleaned_data = form.cleaned_data.copy()
            cleaned_data.pop("confirm_password", None)

            data = CreateUserDataDomain(**cleaned_data)
            success, response = add_user(self.request, data)

            if success:
                messages.success(self.request, f"Username {username} created successfully!")
                return redirect(self.success_url)
            else:
                form.add_error(None, "A user with that username already exists.")
                return self.form_invalid(form)


class UserUpdateView(FormView, NTTDefaultLoginRequiredMixin, SegmentBreadCrumbEnabledMixin):
    template_name = "accounts/user_updateform.html"
    form_class = UserUpdateForm
    success_url = "/accounts/update-user/"

    @property
    def segment(self) -> str:
        return "User Update"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        user_id = self.kwargs.get("user_id")
        return [
            ("Users", reverse("dashboards:users")),
            ("User Update", reverse("accounts:update_user", kwargs={"user_id": user_id})),
        ]

    def get_initial(self):
        user_id = self.kwargs.get("user_id")
        success, response = get_user_for_update(self.request, user_id)
        if success:
            user_data = response.get("data")
            return user_data
        return {}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"] = self.get_initial()
        kwargs["session"] = self.request.session
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        cleaned_data = form.cleaned_data.copy()

        if cleaned_data.get("is_ldap", False) == "True":
            data = UpdateAdUserDataDomain(
                id=user_id, username=cleaned_data.get("username"), groups=cleaned_data.get("groups"), is_ldap=True
            )
            function_api = update_ad_user

        elif "confirm_password" in cleaned_data and not cleaned_data["confirm_password"]:
            cleaned_data.pop("password")
            cleaned_data.pop("confirm_password", None)
            data = UpdateUserWithoutPasswordDataDomain(id=user_id, **cleaned_data)
            function_api = update_user_without_password

        else:
            cleaned_data.pop("confirm_password", None)
            data = UpdateUserDataDomain(id=user_id, **cleaned_data)
            function_api = update_user

        if cleaned_data.get("is_ldap", False) == "True":
            success, response = function_api(self.request, data)
        else:
            success, response = function_api(self.request, data, user_id)

        if success:
            messages.success(self.request, "User updated successfully!")
            return redirect(f"{self.success_url}{user_id}/")
        else:
            response_data = response.get("data", {})
            if response_data.get("username"):
                form.add_error(None, response_data["username"][0])
                return self.form_invalid(form)
            else:
                form.add_error(None, response_data["error"])
            return self.form_invalid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}", extra_tags="danger")
        return redirect(self.request.path_info)


class DeleteUserView(NTTDefaultLoginRequiredMixin, View):
    def delete(self, request, pk):
        success, response = delete_user(request, DeleteUserDataDomain(id=pk))
        if success:
            return HttpResponse(f"User {pk} deleted")

        return HttpResponseBadRequest()


class LocalUserProfileUpdateView(FormView, NTTDefaultLoginRequiredMixin, SegmentBreadCrumbEnabledMixin):
    template_name = "accounts/profile_update.html"
    form_class = LocalUserProfileUpdateForm
    success_url = "/accounts/profile-update/"

    @property
    def segment(self) -> str:
        return "Profile update"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [("Users", reverse("dashboards:users")), ("User Profile", reverse("accounts:profile_update"))]

    def get_initial(self):
        username = self.request.user.username
        success, response = getting_user_profile(self.request, username)
        if success:
            user_data = response.get("data")
            return user_data
        return {}

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        phone = form.cleaned_data["phone"]
        data = GetUserProfileDataDomain(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        files = {"profile_picture": form.cleaned_data["profile_picture"]}
        success, response = updating_user_profile(self.request, data, username, files)
        if success:
            success, response = getting_user_profile(self.request, username)
            if success and form.cleaned_data["profile_picture"]:
                user_data = response.get("data", {})
                self.request.session["profile_picture"] = user_data.get("profile_picture")
                self.request.session.modified = True

            messages.success(self.request, "User updated successfully!")
            return self.render_to_response(self.get_context_data(form=form))
        else:
            form.add_error(None, "Failed to update user.")
            return self.form_invalid(form)


class DeleteMultipleUserView(NTTDefaultLoginRequiredMixin, View):
    def delete(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_ids = data.get("user_ids", [])

            if isinstance(user_ids, list) and all(isinstance(uid, str) for uid in user_ids):
                user_ids = list(map(int, user_ids))

                success, response = delete_users(request, user_ids)

                if success:
                    return HttpResponse(f"Users {user_ids} deleted")

            raise ValueError("Invalid user_ids format")
        except ValueError as e:
            return HttpResponseBadRequest(str(e))


@login_required
def ajax_users(request):
    users = User.objects.exclude(username=request.user.username).values()
    data = {"data": list(users)}

    return JsonResponse(data, safe=False)
