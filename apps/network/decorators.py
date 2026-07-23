from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from apps.users.models import CustomUser


def administrator_required(view_func):
    """
    Decorator for views that require administrator role.
    """

    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != CustomUser.Role.ADMINISTRATOR:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def technician_or_administrator_required(view_func):
    """
    Decorator for views that require either technician or administrator role.
    """

    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role not in [CustomUser.Role.ADMINISTRATOR, CustomUser.Role.TECHNICIAN]:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view
