from typing import Union, Any

from django.db import models
from django.http import HttpRequest
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    InlinePanel,
    MultiFieldPanel,
    FieldRowPanel,
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core import fields, blocks
from wagtail.core.blocks import RawHTMLBlock
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from contrib.columns.blocks import ColumnBlock

from contrib.wagtailmath.blocks import MathjaxBlock


class FormField(AbstractFormField):
    page = ParentalKey("home.EmailFormPage", related_name="form_fields")


class PersonBlock(blocks.StructBlock):
    class Meta:
        icon = "user"
        label = "Person"
        template = "home/blocks/person.html"

    name = blocks.CharBlock(required=True)
    position = blocks.CharBlock(required=True)
    email = blocks.EmailBlock(required=False)
    bio = blocks.RichTextBlock(required=True, features=["bold", "italic"])


class TrombinoscopeBlock(blocks.StructBlock):
    class Meta:
        icon = "user"
        label = "Trombinoscope"
        template = "home/blocks/trombinoscope.html"

    cards = blocks.ListBlock(PersonBlock())


class BasePage(Page):
    class Meta:
        abstract = True

    def get_context(self, request: HttpRequest, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["og"] = BasePage.flatten_object(self.get_opengraph(request))
        context["menu"] = self.get_root().get_children().first().get_children().filter(live=True, show_in_menus=True)
        return context

    def get_opengraph(self, request: HttpRequest):
        # noinspection PyArgumentList
        return {
            "title": self.seo_title or self.title,
            "type": "website",
            "url": self.get_full_url(request),
            "locale": "fr_FR",
            "site_name": self.get_site().site_name,
        }

    @staticmethod
    def flatten_object(obj: Any, sep=":", prefix=""):
        if prefix != "":
            prefix = f"prefix{sep}"
        return {
            f"{prefix}{key}": {value}
            for key, value in dict(obj).items()
        }


class ContentPageBase(BasePage):
    class Meta:
        abstract = True

    content_panels = BasePage.content_panels + [
        StreamFieldPanel("content")
    ]
    template = "home/content_page_base.html"

    content = fields.StreamField(
        [
            ("rich_text", blocks.RichTextBlock(template="home/blocks/rich_text.html")),
            ("image", ImageChooserBlock()),
            ("embed", EmbedBlock()),
            ("raw_html", RawHTMLBlock()),
            ("columns", ColumnBlock()),
            ("mathjax", MathjaxBlock()),
            ("trombinoscope", TrombinoscopeBlock()),
        ],
        blank=True,
        null=True,
    )


class HomePage(ContentPageBase):
    template = "home/landing_page.html"
    max_count = 1


class FlexiblePage(ContentPageBase):
    template = "home/flexible_page.html"
    subpage_types = ["home.FlexiblePage"]
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        StreamFieldPanel("content"),
    ]

    subtitle = models.CharField(max_length=140, blank=True, null=True)


class EmailFormPage(AbstractEmailForm, BasePage):
    template = "home/form_page.html"
    subpage_types = []
    content_panels = Page.content_panels + [
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("confirmation_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                )
            ],
            "Email Notification configuration",
        ),
    ]

    confirmation_text = RichTextField(blank=True)
