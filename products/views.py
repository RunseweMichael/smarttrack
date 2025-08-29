from django.shortcuts import render, redirect
from .models import Products
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import DetailView
from category.models import Category
from django.http import HttpResponse

from openpyxl import Workbook

#pip intsall openpyxl

# Create your views here.
def products_list(request):
    products = Products.objects.all()
    return render(request, 'products/allproducts.html', {'allproducts': products})


@staff_member_required
def create(request):
    if request.method == 'POST':
       name = request.POST['name'] 
       sku = request.POST['sku']
       desc = request.POST['desc']
       price = request.POST['price']
       qty = request.POST['qty']
       img = request.FILES.get('img')
       cat = request.POST['category']

       category = Category.objects.get(name=cat)

       product = Products(name=name, sku=sku, description=desc, category=category, price=price, quantity=qty, image=img)
       product.save()

       category = product.category
       category.quantity = int(category.quantity) + int(product.quantity)
       category.save()

       return redirect('products_list')

    else:
        category = Category.objects.all()

        return render(request, 'products/createproduct.html', {'categories':category})


@staff_member_required
def update(request, id):
    products = Products.objects.get(pk=id)
    category = Category.objects.all()
    initialQuantity = int(products.quantity)

    if request.method == 'POST':
        products.name = request.POST['name']
        products.sku = request.POST['sku']
        products.description = request.POST['desc']
        products.price = request.POST['price']
        products.quantity = request.POST['qty']
        products.image = request.FILES.get('img')
        cat = request.POST['category']
        products.category = Category.objects.get(name=cat)
        
        products.save()


        category = products.category
        updatedQuantity = int(products.quantity)
        finalQuantity = initialQuantity - updatedQuantity
        category.quantity -= finalQuantity
        category.save()

        return redirect('products_list')

    else:
        return render(request, 'products/updateproduct.html', {'update': products, 'categories': category})


@staff_member_required
def delete(request, id):
    product = Products.objects.get(pk=id)
    category = Category.objects.get(name=product.category)
    product.delete()
    product.save()

    category.quantity = category.quantity - product.quantity
    category.save()

    return redirect('products_list')


def export(request):
    products = Products.objects.all()

    wb = Workbook()
    ws = wb.active
    ws.title = 'Smarttrack Products'

    ws.append(["ID", "Name", "SKU", "Description", "Category", "Price", "Quantity"])

    for product in products:
        ws.append([
            product.id,
            product.name,
            product.sku,
            product.description,
            product.category.name,
            product.price,
            product.quantity
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )

    response['Content-Disposition'] = 'attachment; filename=smarttrack_products.xlsx'

    wb.save(response)

    return response



class ProductDetailView(DetailView):
    model = Products
    template_name = 'products/viewdetails.html'
    context_object_name = 'product'