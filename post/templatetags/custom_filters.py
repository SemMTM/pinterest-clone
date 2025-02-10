from django import template
from django.utils.timezone import now, is_naive, make_aware


register = template.Library()


@register.filter
def time_ago(value):
    if not value:
        return ""

    # Ensure `value` is timezone-aware
    if is_naive(value):
        value = make_aware(value)
    current_time = now()
    diff = current_time - value

    # Calculate time differences
    seconds = diff.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    weeks = days / 7
    months = days / 30.44  # Approximate average days in a month
    years = days / 365.25  # Account for leap years

    # Return the appropriate string
    if seconds < 60:
        return f"{int(seconds)} s"
    elif minutes < 60:
        return f"{int(minutes)} m"
    elif hours < 24:
        return f"{int(hours)} h"
    elif days < 7:
        return f"{int(days)} d"
    elif weeks < 4:
        return f"{int(weeks)} w"
    elif months < 12:
        return f"{int(months)} mo"
    else:
        return f"{int(years)} y"


@register.filter(name='force_https')
def force_https(url):
    """ Replaces http:// with https:// in Cloudinary image URLs """
    if url and url.startswith("http://"):
        return url.replace("http://", "https://")
    return url
