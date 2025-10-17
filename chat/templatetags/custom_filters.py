from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """
    Template filter to look up a value in a dictionary.
    Usage: {{ user_completions|lookup:lab.id }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)
