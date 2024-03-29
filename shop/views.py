from django.shortcuts import render, get_object_or_404
from .models import Category, Product

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from cart.forms import CartAddProductForm
# Create your views here.
# to display all products in a given categoru
def product_list (request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)


    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)


    #adding pagination to the category page
    paginator = Paginator.page(categories,7)
    page = request.GET.get('page')
    try:
        cate = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer
        cate = paginator.page(1)
    except EmptyPage:
        cate = paginator.page(paginator.num_pages)


    return render( request, 'shop/product/list.html', 
    {'category':category,
    'categories':categories,
    'products':products,
    'cate':cate})

def product_detail(request,id,slug):
    product = get_object_or_404(Product,id = id, slug=slug,available=True)
    return render(request, 'shop/product/detail.html',{'product':product})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id,
                                         slug=slug,
                                         available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})