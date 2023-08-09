from products.views.contact import ProductsContactView
from products.views.index import ProductsIndexView
from products.views.search import ProductSearchView
from products.views.shop import ProductsCategoryView
from products.views.shop import ProductsDetailView
from products.views.shop import ProductsReviewView
from products.views.shop import ProductsShopView


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
