from dataclasses import dataclass
from uuid import UUID
from uuid import uuid4

from app.services import BaseService
from products.models import Category
from products.models import Product


@dataclass
class ProductCreator(BaseService):
    name: str
    category: Category | list[Category]
    short_description: str = "No short description"
    description: str = "No description"
    information: str = "No information"
    available: bool = True
    public_id: UUID | None = None

    def __post_init__(self) -> None:
        self.public_id = self.public_id if self.public_id is not None else uuid4()
        self.category = self.category if isinstance(self.category, list) else [self.category]

    def act(self) -> Product:
        return self.create()

    def create(self) -> Product:
        product = Product.objects.create(
            name=self.name,
            # category will be added below
            short_description=self.short_description,
            description=self.description,
            information=self.information,
            available=self.available,
            public_id=self.public_id,
        )
        product.category.add(*self.category)  # because category is m2m field

        return product
