from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def compress_and_convert_to_jpeg(image, max_size=(1000, 1000), quality=80):
    """
    Compresses and converts an image to JPEG format before saving.
    - Resizes images larger than max_size.
    - Converts PNG/WebP images to JPEG.
    - Compresses the JPEG file.
    """

    # Open the image using Pillow
    img = Image.open(image)

    # Convert to RGB mode (required for JPEG)
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Resize image if it's larger than max_size
    img.thumbnail(max_size)

    # Save the image as JPEG in memory
    img_io = BytesIO()
    img.save(img_io, format="JPEG", quality=quality)  # Compress & save as JPEG

    # Create a new InMemoryUploadedFile to replace the original image
    new_image = InMemoryUploadedFile(
        img_io,           # File object
        "ImageField",     # Field name
        f"{image.name.split('.')[0]}.jpg",  # New file name
        "image/jpeg",     # MIME type
        img_io.tell(),    # File size
        None              # Optional charset
    )
    return new_image
