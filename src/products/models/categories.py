from django.urls import reverse
from django.utils.text import slugify

from app.models import TimestampedModel, models


#! class CategoryManager(models.Manager):
#!     def create_category(self, category, slug):
#!         cat = self.create(category=category, slug=category)
#!         return cat


class Category(TimestampedModel):
    CATEGORY_CHOICES = [
        (None, 'Select category'),
        
        ('Dresses', (
                ('man', 'Men\'s Dresses'),
                ('woman', 'Women\'s Dresses'),
                ('baby', 'Baby\'s Dresses'),
            )
        ),

        ('shirts', 'Shirts'),
        ('jeans', 'Jeans'),
        ('swimwear', 'Swimwear'),
        ('sleepwear', 'Sleepwear'),
        ('sportswear', 'Sportswear'),
        ('jumpsuits', 'Jumpsuits'),
        ('blazers', 'Blazers'),
        ('jackets', 'Jackets'),
        ('shoes', 'Shoes'),
    ]

    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, db_index=True)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='category', blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def get_absolute_url(self):
        return reverse("products:category", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Category, self).delete(*args, **kwargs)
        storage.delete(path)

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ''
    
    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = 'Categories'
        # ordering = ['category']
        # TODO: find how to sort by CATEGORY_CHOICES
