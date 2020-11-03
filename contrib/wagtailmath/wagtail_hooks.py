import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.core import hooks


@hooks.register("register_rich_text_features")
def register_mark_feature(features):
    feature_name = "latex-inline"
    type_ = "MARK"
    control = {
        "type": type_,
        "label": "TeX",
        "description": "Inline LaTeX",
        "style": {"font-family": "monospace"}
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {"span.mathjax": InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": "span", "props": {"class": "mathjax"}}}},
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)
