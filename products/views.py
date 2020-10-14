from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


def all_products(request):
    """ View to return all products """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ Return individual product and pass as context to product_detail.html """

    product = get_object_or_404(Product, pk=product_id)
    context = {
        'products': product,
    }

    return render(request, 'products/product_detail.html', context)
