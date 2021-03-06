# Generated by Django 2.2.16 on 2020-09-06 13:10

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_formfield_clean_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flexiblepage',
            name='content',
            field=wagtail.core.fields.StreamField([('rich_text', wagtail.core.blocks.RichTextBlock()), ('raw_html', wagtail.core.blocks.RawHTMLBlock()), ('person', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(required=True)), ('position', wagtail.core.blocks.CharBlock(required=True)), ('email', wagtail.core.blocks.EmailBlock(required=False)), ('bio', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic'], required=True))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=wagtail.core.fields.StreamField([('rich_text', wagtail.core.blocks.RichTextBlock()), ('raw_html', wagtail.core.blocks.RawHTMLBlock()), ('trombinoscope', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(required=True)), ('position', wagtail.core.blocks.CharBlock(required=True)), ('email', wagtail.core.blocks.EmailBlock(required=False)), ('bio', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic'], required=True))])))]))], blank=True, null=True),
        ),
    ]
