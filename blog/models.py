from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.core.blocks import RichTextBlock
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail_pygments import blocks as pygments_blocks
from wagtail.search import index


class CodeBlock(pygments_blocks.CodeBlock):
    class Meta:
        icon = "code"
        value_class = pygments_blocks.CodeStructValue
        template = "blocks/code_block.html"


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.BlogPage']

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        articles = self.get_children().live().order_by('-first_published_at')
        context['articles'] = articles
        return context


class BlogAuthor(Orderable):
    page = ParentalKey("blog.BlogPage", related_name="authors")
    name = models.CharField(default="Anonymous", max_length=50)
    email = models.EmailField(null=True, blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("email")
    ]


class BlogPage(Page):
    date = models.DateField('Post date')
    intro = models.CharField(max_length=250)

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
        MultiFieldPanel([InlinePanel("authors", min_num=1)], heading="Auteurs"),
        FieldPanel('intro'),
        StreamFieldPanel('content')
    ]
