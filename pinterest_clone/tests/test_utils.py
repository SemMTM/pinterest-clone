from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io


def generate_test_image():
    """Generate a valid in-memory image for testing."""
    image = Image.new('RGB', (100, 100), color='red')
    img_io = io.BytesIO()
    image.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile("test_image.jpg",
                              img_io.getvalue(),
                              content_type="image/jpeg")