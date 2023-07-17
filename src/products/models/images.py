from app.models import TimestampedModel, models
from app.files import RandomFileName
from products.models import Category, Product


class Image(TimestampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')  # related_query_name='images'
    image = models.ImageField(upload_to=RandomFileName(r'product/%Y/%m/%d/'))  # may be name "src" would be better FIXME: look at product/%Y/%m/%d/ folder 0_o
    
    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Category, self).delete(*args, **kwargs)
        storage.delete(path)

    def __str__(self):
        return self.image.name
    
    def get_absolute_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ''
    
    # class Meta:
    #     default_related_name = 'images'
