from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    MultiFieldPanel,
    InlinePanel,
    FieldPanel,
    StreamFieldPanel,
)

from wagtail.core.models import Page, Orderable
from wagtail.core import fields, blocks


class Link(Orderable):
    class Meta:
        verbose_name = "Lien"

    entry_title = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Peut être laissé vide, il sera alors affiché le lien, ou le titre de la page interne",
        verbose_name="Titre",
    )
    link_internal = models.ForeignKey(
        "wagtailcore.Page",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Ce lien sera utilisé en priorité si défini",
        verbose_name="Lien interne",
    )
    link_external = models.URLField(
        blank=True,
        null=True,
        help_text="AJoutez un lien externe ici. Il sera utilisé si aucun lien interne n'est défini.",
        verbose_name="Lien externe",
    )
    page = ParentalKey("HomePage", related_name="links", on_delete=models.PROTECT)

    @property
    def link(self):
        if self.link_internal:
            return self.link_internal.url
        elif self.link_external:
            return self.link_external
        return "#"

    @property
    def name(self):
        if self.link_internal and not self.entry_title:
            return self.link_internal.title
        elif self.entry_title:
            return self.entry_title
        return self.link_external


class HomePage(Page):
    template = "home/landing_page.html"
    content_panels = Page.content_panels + [
        InlinePanel("links", label="Liens", min_num=1),
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
