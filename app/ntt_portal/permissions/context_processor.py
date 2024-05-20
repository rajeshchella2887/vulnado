from ntt_portal.permissions.ntt_roles import determine_role
from ntt_portal_library.domains.accounts import UserSessionDataDomain


def auth(request):
    if not hasattr(request, "session"):
        raise RuntimeError("session data is not available")

    if not request.session.get("role"):
        return {}

    user_session_data = UserSessionDataDomain(
        **{
            "access": request.session.get("access"),
            "refresh": request.session.get("refresh"),
            "role": request.session.get("role"),
            "all_permissions": request.session.get("all_permissions"),
            "user_permissions": request.session.get("user_permissions"),
            "groups": request.session.get("groups"),
        }
    )

    # NOTE: role takes priority
    if not user_session_data.role:
        return {}

    defined_role = determine_role(user_session_data.role)

    # NOTE: additional permissions are dynamic
    additional_permissions = {perm: True for perm in user_session_data.user_permissions}

    return {
        "ntt_perms": {
            **defined_role.available_permissions,
            **additional_permissions,
        },
    }
