import os.path
from io import StringIO, BytesIO
from typing import BinaryIO

from django.core.files.base import ContentFile
from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import AbstractRendition

from contrib.opengraph.gen import assemble


@register_setting(icon="media")
class OpenGraphSettings(BaseSetting):
    class Meta:
        verbose_name = verbose_name_plural = "paramètres OpenGraph"

    default_bg_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL,
                                         related_name="+")

    panels = [ImageChooserPanel("default_bg_image")]


def upload_og_image(instance: "OpenGraphRendition", filename: str) -> str:
    filename = instance.rendered.field.storage.get_valid_name(filename)
    return os.path.join("og_images", filename)


class OpenGraphRendition(models.Model):
    key = models.CharField(max_length=256, primary_key=True)
    rendered = models.ImageField(upload_to=upload_og_image, width_field="width", height_field="height")
    width = models.IntegerField()
    height = models.IntegerField()

    def get_object_url(self):
        return self.rendered.url

    @classmethod
    def create_rendition(cls, background: BinaryIO, key: str, title: str) -> "OpenGraphRendition":
        from PIL.Image import open

        try:
            return cls.objects.get(key=key)
        except cls.DoesNotExist:
            with open(background) as bg:
                rendition = assemble(bg, title)
            img_io = BytesIO()
            rendition.convert("RGB").save(img_io, format="JPEG", quality=90)
            img_content = ContentFile(img_io.getvalue(), f"rendition_{key}.jpg")

            rendition = OpenGraphRendition(key=key, rendered=img_content)
            rendition.save()
            return rendition
