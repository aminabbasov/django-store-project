import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from app.files import RandomFileName
from products.models import Image


@pytest.fixture
def product(mixer):
    return mixer.blend("products.Product")


@pytest.fixture
def filename():
    return RandomFileName(r"product/%Y/%m/%d/")


@pytest.fixture
def image_file(filename):
    return SimpleUploadedFile(filename("", "test_image.jpg"), b"file_content", content_type="image/jpeg")


@pytest.fixture
def image(mixer, product, image_file):
    return mixer.blend("products.Image", product=product, image=image_file)


@pytest.mark.django_db
def test_image_model_delete(image, product):
    image_path = image.image.path
    image.delete()
    assert not Image.objects.filter(pk=image.pk).exists()  # Image should be deleted from the database
    assert not image.image.storage.exists(image_path)      # Image file should be deleted from storage
    assert not product.images.count()                      # No images should be associated with the product
