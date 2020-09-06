from django.db import models

from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core.fields import RichTextField
from wagtail.core.blocks import RichTextBlock
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail_pygments.blocks import CodeBlock
from wagtail.search import index


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    subpage_types = ['blog.BlogPage']

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        articles = self.get_children().live().order_by('-first_published_at')
        context['articles'] = articles
        return context


class AuthorBlock(blocks.StructBlock):
    class Meta:
        icon = "user"
    name = blocks.CharBlock(required=False, default="Unknown", max_length=50)
    email = blocks.EmailBlock(required=False)


class BlogPage(Page):
    date = models.DateField('Post date')
    intro = models.CharField(max_length=250)

    authors = StreamField([
        ('author', AuthorBlock())
    ], null=True)

    content = StreamField([
        ('rich_text', RichTextBlock()),
        ('code', CodeBlock())
    ])

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('content')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        StreamFieldPanel('authors'),
        FieldPanel('intro'),
        StreamFieldPanel('content')
    ]
