
```sql

SELECT
    DISTINCT sku_id
FROM
    ProductVariantSKU
WHERE
    value in :form
    AND
    attribute_id in :product_variants;

```

```py

class SIZES(models.TextChoices):        
    __empty__ = _('Select size')

    XS = 'XS', 'XS'
    S = 'S', 'S'
    M = 'M', 'M'
    L = 'L', 'L'
    XL = 'XL', 'XL'
       
class COLORS(models.TextChoices):
    __empty__ = _('Select color')
    
    BLACK = 'black', _('Black')
    WHITE = 'white', _('White')
    RED = 'red', _('Red')
    BLUE = 'blue', _('Blue')
    GREEN = 'green', _('Green')

```
