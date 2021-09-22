import logging

from django.forms import Widget, CharField
from django.templatetags.static import static
from django.utils.functional import lazy
from wagtail.core.blocks import FieldBlock
from wagtail.core.telepath import register
from wagtail.core.widget_adapters import WidgetAdapter

static_lazy = lazy(static, str)

logger = logging.getLogger(__name__)


class MathJaxWidget(Widget):
    class Media:
        js = (
            "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js",
        )

    template_name = "wagtailmath/mathjax_widget.html"

    def get_context(self, name, value, attrs):
        return {
            "widget": {
                "name": name,
                "is_hidden": self.is_hidden,
                "required": self.is_required,
                "value": value,
                "attrs": self.build_attrs(attrs),
                "template_name": self.template_name,
            }
        }


class MathJaxAdapter(WidgetAdapter):
    js_constructor = "contrib.wagtailmath.blocks.MathJaxWidget"

    def js_args(self, _: MathJaxWidget):
        return []

    class Media:
        js = [static_lazy("wagtailmath/js/wagtailmath.js")]


register(MathJaxAdapter(), MathJaxWidget)


class MathjaxBlock(FieldBlock):
    class Meta:
        template = "wagtailmath/mathjax_block.html"
        name = "MathJax equation"

    class Media:
        js = (
            "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js",
            static_lazy("wagtailmath/js/wagtailmath.public.js"),
        )

    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = CharField(required=required, help_text=help_text, widget=MathJaxWidget())
        super().__init__(**kwargs)

    def value_from_form(self, value):
        logger.info("Value: %s" % repr(value))
        return value
