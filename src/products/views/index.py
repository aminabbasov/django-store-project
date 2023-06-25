from django.views import generic


# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
from django.db.models import Case, When, Value, IntegerField, Count
from products.models import Category, Product

class IndexServices:
    def get_carousel_categories(self):
        carousel_categories = Category.objects.filter(category__in=['man', 'woman', 'baby']).order_by(
                Case(
                    When(category='man', then=Value(1)),
                    When(category='woman', then=Value(2)),
                    When(category='baby', then=Value(3)),
                    output_field=IntegerField(),
                )
            )
        return carousel_categories

    def get_main_discount_products(self):
        main_discount_products = Product.objects.filter(discount__gt=0).order_by('-discount')[:2]
        return main_discount_products

    def get_second_discount_products(self):
        second_discount_products = Product.objects.filter(discount__gt=0).order_by('-created')[:2]
        return second_discount_products

    def get_categories(self):
        categories = Category.objects.annotate(amount=Count('product'))
        return categories

    def get_featured_products(self):
        featured_products = Product.objects.annotate()[:4]
        return featured_products

    def get_recent_products(self):
        recent_products = Product.objects.annotate().order_by('-created')[:4]
        return recent_products
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX

class ProductsIndexView(generic.TemplateView):
    template_name = 'products/index.html'

    def setup(self, request, *args, **kwargs):
        super(ProductsIndexView, self).setup(request, *args, **kwargs)
        self.service = IndexServices()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['carousel']          = self.service.get_carousel_categories()
        context['main_discount']     = self.service.get_main_discount_products()
        context['second_discount']   = self.service.get_second_discount_products()
        context['categories']        = self.service.get_categories()
        context['featured_products'] = self.service.get_featured_products()
        context['recent_products']   = self.service.get_recent_products()

        return context
