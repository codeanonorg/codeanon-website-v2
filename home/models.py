from django.db import models
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
)
from wagtail.core import fields, blocks
from wagtail.core.models import Page, Orderable


class HomePage(Page):
    template = "home/landing_page.html"
    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]
    content = fields.StreamField(
        [("rich_text", blocks.RichTextBlock()), ("raw_html", blocks.RawHTMLBlock())],
        blank=True,
        null=True,
    )


class FlexiblePage(Page):
    template = "home/flexible_page.html"
    subpage_types = ["home.FlexiblePage"]
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        StreamFieldPanel("content"),
    ]

    subtitle = models.CharField(max_length=140, blank=True, null=True)
    content = fields.StreamField(
        [("rich_text", blocks.RichTextBlock()), ("raw_html", blocks.RawHTMLBlock())],
        blank=True,
        null=True,
    )
