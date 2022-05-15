import datetime
from django.conf import settings


def set_cookie(response, key, value, day_expire=7):
    if day_expire is None:
        max_age = 365*24*60*60
    else:
        max_age = day_expire * 24 * 60 *60

    expires = datetime.datetime.strftime(datetime.datetime.utcnow()
                                         + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT",)
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None
    )