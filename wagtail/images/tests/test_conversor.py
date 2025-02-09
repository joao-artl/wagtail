from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from wagtail.images.models import get_image_model
from wagtail.images.conversor import CustomImage

class ImageConversion(TestCase):
    def ImageConversionTest(self):
        Image = get_image_model()
        image = SimpleUploadedFile("test.jpg", b"fake_image_data", content_type="image/jpeg")
        obj = Image.objects.create(title="Teste", file=image)
        self.assertTrue(obj.avif_file, "O arquivo AVIF não foi gerado.")

    def WebPFallbackTest(self):
        Image = get_image_model()
        image = SimpleUploadedFile("test.jpg", b"fake_image_data", content_type="image/jpeg")
        obj = Image.objects.create(title="Teste", file=image)
        response = self.client.get(f"/serve-image/{obj.id}", HTTP_ACCEPT="image/webp")
        self.assertEqual(response["Content-Type"], "image/webp")