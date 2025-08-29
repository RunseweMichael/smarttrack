from django.shortcuts import render, redirect
from .models import Category
from products.models import Products

# Create your views here.

def allcategories(request):
    category = Category.objects.all()

    return render(request, 'category/allcategories.html', {"categories":category})


def createcategory(request):
    if request.method == "POST":
        name = request.POST['name']
        slug = request.POST['slug']
        desc = request.POST['desc']
        qty = request.POST['qty']

        category = Category(name=name, slug=slug, description=desc,quantity=qty)

        category.save()
        return redirect('allcategories')

    else:
        return render(request, 'category/createcategory.html')


def updatecategory(request, id):
    category = Category.objects.get(pk=id)

    if request.method=='POST':
        category.name = request.POST['name']
        category.slug = request.POST['slug']
        category.description = request.POST['desc']

        category.save()

        return redirect('allcategories')
    
    else:
        return render(request, 'category/updatecategory.html', {'category':category})



def deletecategory(request, id):
    category = Category.objects.get(pk=id)

    category.delete()

    return redirect('allcategories')



def searchcategory(request):
    category = Category.objects.all()

    if request.method=='POST':
        category = request.POST['category']

        category_object = Category.objects.get(name=category)

        products = Products.objects.filter(category = category_object)

        return render (request, 'category/searchcategory.html', {'products': products})

    else:
        return render(request, 'category/searchcategory.html', {'categories': category})