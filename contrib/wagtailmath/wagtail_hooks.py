import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.core import hooks


@hooks.register("register_rich_text_features")
def register_mark_feature(features):
    tag = "latex-inline"
    control = {
        "type": tag,
        "label": "TeX",
        "description": "Inline LaTeX",
        "element": "span",
        "style": {"font-family": "monospace", "background-color": "#CCC"}
    }

    features.register_editor_plugin(
        "draftail", tag, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {"span[class=mathjax]": InlineStyleElementHandler(tag)},
        "to_database_format": {"style_map": {tag: {"element": "span", "props": {"class": "mathjax"}}}},
    }

    features.register_converter_rule("contentstate", tag, db_conversion)

    features.default_features.append(tag)
