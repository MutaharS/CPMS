from django.shortcuts import render
from .models import Product
from .forms import ProductForm

# Create your views here.
def product_create_view(request):
    context = {}
    # Get form data and save it into database as follows
    # if(request.method == POST)
    #   newInfo = request.POST.get('info')
    #   Product.objects.create(info=newInfo)
    return render(request,"product/product_create.html", context)

def product_detail_view(request):
    obj = Product.objects.get(id=1)
    context = {
        'object': obj
    }
    return render(request,"product/product_detail.html", context)