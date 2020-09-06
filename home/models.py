from django.db import models
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
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable


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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["menu"] = self.get_root().get_children().first().get_children().filter(live=True, show_in_menus=True)
        return context


class HomePage(BasePage):
    template = "home/landing_page.html"
    max_count = 1
    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]
    content = fields.StreamField(
        [("rich_text", blocks.RichTextBlock()), ("raw_html", blocks.RawHTMLBlock()),
         ("trombinoscope", TrombinoscopeBlock())],
        blank=True,
        null=True,
    )


class FlexiblePage(BasePage):
    template = "home/flexible_page.html"
    subpage_types = ["home.FlexiblePage"]
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        StreamFieldPanel("content"),
    ]

    subtitle = models.CharField(max_length=140, blank=True, null=True)
    content = fields.StreamField(
        [("rich_text", blocks.RichTextBlock()), ("raw_html", blocks.RawHTMLBlock()), ("person", TrombinoscopeBlock())],
        blank=True,
        null=True,
    )


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
