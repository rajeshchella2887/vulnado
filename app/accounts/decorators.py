from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect, reverse


def logged_in_user(session_data):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if "access" in request.session and "access" in session_data:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(reverse("accounts:login-user"))  # Use reverse to get the URL

        return wrapper_func

    return decorator


def user_permissions(permission):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_permissions_session = request.session.get("permissions")
            if permission in user_permissions_session:
                # User is authenticated and has the required permission
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You don't have permission to perform this action.")

        return wrapper

    return decorator
