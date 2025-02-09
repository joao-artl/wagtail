from wagtail.images.models import Image
from django.db import models
from django.http import FileResponse
from django.shortcuts import get_object_or_404
import io
from PIL import Image as PILImage


class CustomImage(Image):
    avif_file = models.FileField(upload_to="images/avif/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.convert_to_avif()
        super().save(*args, **kwargs)

    def convert_to_avif(self):
        img = PILImage.open(self.file)
        avif_buffer = BytesIO()
        img.save(avif_buffer, format="AVIF", quality=80)
        self.avif_file.save(f"{self.title}.avif", avif_buffer, save=False)

    def serve_image(request, image_id):
        image = get_object_or_404(CustomImage, id=image_id)
        accept_header = request.headers.get('Accept', '')

        if "image/avif" in accept_header and image.avif_file:
            return FileResponse(image.avif_file.open(), content_type="image/avif")
        elif "image/webp" in accept_header:
            webp_buffer = io.BytesIO()
            img = PILImage.open(image.file)
            img.save(webp_buffer, format="WEBP", quality=80)
            return FileResponse(io.BytesIO(webp_buffer.getvalue()), content_type="image/webp")
        else:
            return FileResponse(image.file.open(), content_type=image.file.content_type)