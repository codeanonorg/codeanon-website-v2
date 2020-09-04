from django.db import models
from django.http import HttpRequest
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    InlinePanel,
    MultiFieldPanel,
    FieldRowPanel,
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
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


class ArticlePage(Page):
    template = "home/article.html"
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("intro"),
        StreamFieldPanel("content"),
    ]

    subtitle = models.CharField(max_length=140)
    intro = RichTextField(features=["bold", "italics"])

    content = fields.StreamField(
        [("rich_text", blocks.RichTextBlock()), ("raw_html", blocks.RawHTMLBlock())]
    )

    @property
    def wordcount(self):
        return sum(len(str(b.value).split()) for b in self.content)


class ArticleIndexPage(RoutablePageMixin, Page):
    subpage_types = ["home.ArticlePage"]
    content_panels = Page.content_panels + [
        FieldPanel("intro")
    ]
    intro = RichTextField(null=True, blank=True)

    @route(r"^$")
    def last_articles(self, request: HttpRequest):
        articles = ArticlePage.objects.live().order_by('-first_published_at')

        return render(request, "home/article_index.html", {
            'title': "Derniers articles",
            'self': self,
            'page': self,
            'articles': articles
        })

    @route(r"^(\d+)$")
    def year_articles(self, request: HttpRequest, year: int):
        articles = ArticlePage.objects.live().filter(first_published_at__year=year)

        return render(request, "home/article_index.html", {
            'title': f"Articles de {year}",
            'self': self,
            'page': self,
            'articles': articles,
        })

    @route(r"^((?:\w|\s)+)$")
    def tag_articles(self, request, tag):
        articles = ArticlePage.objects.live().filter(tags__name=tag)

        return render(request, "home/article_index.html", {
            'title': f"Articles sur {tag}",
            'self': self,
            'page': self,
            'articles': articles
        })
