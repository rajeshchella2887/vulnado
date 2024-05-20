from accounts.apis import getting_user_profile, user_login
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from ntt_portal_library.contracts.api_contracts.accounts.user_login_contract import UserLoginDataDomain
from ntt_portal_library.domains.accounts import UserSessionDataDomain


class NTTAuthBackend(BaseBackend):
    """
    Authenticate against auth_service

    TODO: we need to determine if user is super user or staff

    """

    def authenticate(self, request, username=None, password=None):
        success, response = user_login(UserLoginDataDomain(username=username, password=password))

        if not success:
            return None

        data = response.data.to_dict()

        user = User.objects.filter(username__iexact=username).first()
        if not user:
            # TODO: determine user staff/superuser status from response
            # NOTE: safer to list down what we want instead of excluding
            fields_to_assign = (
                "username",
                "email",
                "first_name",
                "last_name",
                "last_login",
                "is_superuser",
                "is_staff",
                "is_active",
                "date_joined",
            )

            assignment_dict = {field: value for field, value in data.items() if field in fields_to_assign}

            user = User(**assignment_dict)
            user.save()

        # NOTE: Rahul's session code
        user_session_data = UserSessionDataDomain(
            access=response.data.access,
            refresh=response.data.refresh,
            role=response.data.role,
            groups=response.data.groups,
            user_permissions=response.data.user_permissions,
        )

        request.session.update({**user_session_data.to_dict()})
        success, response = getting_user_profile(request, username)
        if success:
            user_data = response.get("data")
            profile_picture_data = {"profile_picture": user_data.get("profile_picture")}
            request.session.update(profile_picture_data)
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
