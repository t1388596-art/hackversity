"""
Safe static files template tags
"""

from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def safe_static(path):
    """
    Load static file safely - returns empty string if file doesn't exist
    Usage: {% safe_static 'images/favicon.ico' %}
    """
    try:
        # Try to get the URL using the static files storage
        url = staticfiles_storage.url(path)
        return url
    except (ValueError, FileNotFoundError, Exception) as e:
        # If file doesn't exist in manifest or filesystem, return empty string
        # This prevents the "Missing staticfiles manifest entry" error
        return ''

@register.simple_tag
def safe_static_or_default(path, default=''):
    """
    Load static file safely with a default fallback
    Usage: {% safe_static_or_default 'images/favicon.ico' '/static/images/default-favicon.ico' %}
    """
    try:
        url = staticfiles_storage.url(path)
        return url
    except (ValueError, FileNotFoundError, Exception):
        return default