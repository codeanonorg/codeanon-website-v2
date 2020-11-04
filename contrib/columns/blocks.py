from wagtail.core.blocks import StructBlock, StreamBlock, RichTextBlock, RawHTMLBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class ColumnBlock(StructBlock):
    class Meta:
        icon = "doc-full"
        label = "Columns"
        template = "columns/block.html"

    columns = StreamBlock(
        [
            ("paragraph", RichTextBlock(template="columns/column_rich_text.html")),
            ("image", ImageChooserBlock()),
            ("embed", EmbedBlock()),
            ("raw_html", RawHTMLBlock())
        ]
    )