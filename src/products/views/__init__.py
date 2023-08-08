from .contact import ProductsContactView
from .index import ProductsIndexView
from .search import ProductSearchView
from .shop import ProductsCategoryView
from .shop import ProductsDetailView
from .shop import ProductsReviewView
from .shop import ProductsShopView


__all__ = [
    # index
    "ProductsIndexView",
    # contact
    "ProductsContactView",
    # shop
    "ProductsShopView",
    "ProductsCategoryView",
    "ProductsDetailView",
    "ProductsReviewView",
    # search
    "ProductSearchView",
]
