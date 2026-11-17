
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import never_cache


# ==========================================
# BUYER-ONLY ACCESS
# ==========================================

def buyer_required(view_func):

    @login_required(login_url='login')
    @never_cache
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.role != 'buyer':
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


# ==========================================
# SELLER-ONLY ACCESS
# ==========================================

def seller_required(view_func):

    @login_required(login_url='login')
    @never_cache
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.role != 'seller':
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper
