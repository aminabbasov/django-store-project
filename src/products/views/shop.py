from django.views import generic
from django.contrib import messages
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.mixins import LoginRequiredMixin

from products.models import Product
from products.forms import ProductsReviewForm


# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
from django.db.models import Avg

class ShopServices:
    def get_products(self):
        products = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
        return products
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX

class ProductsShopView(generic.ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/shop.html'
    paginate_by = 3
    
    def setup(self, request, *args, **kwargs):
        super(ProductsShopView, self).setup(request, *args, **kwargs)
        self.service = ShopServices()
    
    def get_paginate_by(self, queryset):
        self.paginate_by = self.request.GET.get("paginate_by", self.paginate_by)  # example: ?paginate_by3&page=2
        return self.paginate_by
    
    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        try:
            return super(ProductsShopView, self).paginate_queryset(queryset, page_size)
        except Http404:
            self.kwargs['page'] = paginator.num_pages

            # self.request.GET['page'] = 1  # FIX INCORRECT URL ON PAGE RESET!!!
            return super(ProductsShopView, self).paginate_queryset(queryset, page_size)
    
    def get_queryset(self):
        queryset = self.service.get_products()
        
        ordering = self.get_ordering()
        if ordering and isinstance(ordering, str):
            ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
            
        filtering = self._get_filtering()
        queryset = queryset.filter(filtering)

        return queryset  #! УПОРЯДОЧИТЬ QUERYSET .order_by('name')                                   XXXXXXXXXXXXXXXXXXXXXX
        
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['paginate_by']    = self.paginate_by
        context['selected_price'] = self.request.GET.getlist('price_filter')
        context['selected_color'] = self.request.GET.getlist('color_filter')
        context['selected_size']  = self.request.GET.getlist('size_filter')
        
        return context

    def get_ordering(self):
        ordering  = self.request.GET.get('sort', None)

        if ordering == 'latest':
            return '-date'
        elif ordering == 'popularity':
            return 'views'
        elif ordering == 'rating':
            return '-avg_rating'

        return ordering

    def _get_filtering(self):
        price_values = {
            '1-100':   {'price__range': (0.01, 100)},
            '100-200': {'price__range': (101.01, 200)},
            '200-300': {'price__range': (201.01, 300)},
            '300-400': {'price__range': (301.01, 400)},
            '400+':    {'price__gte': 401.01},
        }

        price_q, color_q, size_q = Q(), Q(), Q()

        for price in self.request.GET.getlist('price_filter'):
            if price:
                price_q |= Q(**price_values[price])
        
        for color in self.request.GET.getlist('color_filter'):
            if color:
                color_q |= Q(color__iexact=color)

        for size in self.request.GET.getlist('size_filter'):
            if size:
                size_q |= Q(size__iexact=size)

        q_filters = price_q & color_q & size_q
        return q_filters


class ProductsCategoryView(ProductsShopView):
    def get_queryset(self):
        queryset = super(ProductsCategoryView, self).get_queryset()
        slug = self.kwargs.get('slug')
        queryset = queryset.filter(category__slug=slug)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['category'] = self.kwargs.get('slug')

        return context


# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
class ProductServices:
    def get_related_products(self, categories):
        related_products = Product.objects.filter(category__in=categories)[:5]
        return related_products
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX

class ProductsDetailView(generic.DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    
    def setup(self, request, *args, **kwargs):
        super(ProductsDetailView, self).setup(request, *args, **kwargs)
        self.service = ProductServices()
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['related_products'] = self.service.get_related_products(categories=self.object.category.all())
        context['review_form'] = ProductsReviewForm(
            instance=self.get_object()
        )

        return context
    
    def post(self, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['pk'])

        if int(self.request.POST['quantity']) < 1:
            messages.error(self.request, 'Can\'t add less than one product.')
    
            return redirect('products:detail', pk=self.kwargs['pk'])

        try:
            self.request.cart.add(
                product=product,
                size=self.request.POST['size'],
                color=self.request.POST['color'],
                quantity=int(self.request.POST['quantity'])
            )
            messages.success(self.request, 'Product added to cart.')

        except MultiValueDictKeyError:
            messages.error(self.request, 'Please select an options.')

        except Exception:
            #! logger.error('Product cannot be added to cart.', exc_info=True)                           XXXXXXXXXXXXXXXXXXXXXX
            messages.error(self.request, 'Something went wrong, please try again later.')

        return redirect('products:detail', pk=self.kwargs['pk'])


class ProductsReviewView(LoginRequiredMixin, generic.FormView):
    template_name = 'products/detail.html'
    http_method_names = ['post']
    form_class = ProductsReviewForm

    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        review = form.save(commit=False)
        review.product_id = self.kwargs['pk']
        review.user_id = self.request.user.pk
        review.save()
        messages.success(self.request, 'You left a comment. Thank you!')

        return super(ProductsReviewView, self).form_valid(form)
    
    def form_invalid(self, form):
        if form.errors:
            for error in form.errors.values():
                messages.error(self.request, error)

        return redirect('products:detail', pk=self.kwargs['pk'])
