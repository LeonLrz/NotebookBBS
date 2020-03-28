from flask import session, redirect, url_for,g
from functools import  wraps
import config


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if config.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("cms.login"))
    return inner


def permission_required(permission):
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.unauth'))
        return inner
    return outer
