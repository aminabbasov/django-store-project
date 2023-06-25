from app.models import Timestamped, models
from products.models import Category, Product


class Image(Timestamped):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')  # related_query_name='images'
    image = models.ImageField(upload_to=r'product/%Y/%m/%d/')
    
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
  