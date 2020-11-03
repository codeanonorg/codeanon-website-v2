from django import template

register = template.Library()


@register.simple_tag
def mathjax():
    return "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"
