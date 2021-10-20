from typing import Any

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


def flatten_obj(obj: dict[str, Any], sep=":", prefix="") -> dict[str, Any]:
    values = []
    for key, obj in obj.items():
        if len(prefix) > 0:
            key = f"{prefix}{sep}{key}"
        if isinstance(obj, dict):
            values += list(flatten_obj(obj, sep, key).items())
        else:
            values.append((key, obj))
    return dict(values)


@register.filter
def opengraph(value: dict[str, Any]):
    tags = flatten_obj(value, prefix="og")
    return mark_safe("\n".join(
        [f'<meta property="{conditional_escape(key)}" content="{conditional_escape(val)}" />' for key, val in
         tags.items()]))
