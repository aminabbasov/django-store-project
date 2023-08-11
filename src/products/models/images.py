from typing import Any

from app.files import RandomFileName
from app.models import models
from app.models import TimestampedModel
from products.models.products import Product


class Image(TimestampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=RandomFileName(r"product/%Y/%m/%d/"))  # may be name "src" would be better

    def delete(self, *args: Any, **kwargs: dict[str, Any]) -> Any:
        storage, path = self.image.storage, self.image.path
        storage.delete(path)
        return super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.image.name

    def get_absolute_url(self) -> str:
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        return ""
