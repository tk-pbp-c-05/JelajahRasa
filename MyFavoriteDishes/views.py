# MyFavoriteDishes/views.py

import json
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from .models import Food, FavoriteDish
from .forms import FavoriteDishForm
from .forms import FavoriteDishFromCatalogueForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages

@login_required
def show_favorite(request):
    favorite_dishes = FavoriteDish.objects.filter(user=request.user)

    context = {
        'name': request.user.username,
        'favorite_dishes':favorite_dishes,
    }
    return render(request, 'show_favorite.html', context)

def access_favorite(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view favorite dishes.")
        return redirect('main:login')  # Adjust to your login URL name
    return show_favorite(request)

def add_favorite(request):
    if request.method == 'POST':
        form = FavoriteDishFromCatalogueForm(request.POST)
        if form.is_valid():
            food = form.cleaned_data['food']  
            favorite_dish = FavoriteDish(
                user=request.user,
                food=food,
                name=food.name, 
                flavor=food.flavor,
                category=food.category,  
                vendor_name=food.vendor_name,  
                price=food.price,  
                map_link=food.map_link,  
                address=food.address,
                image=food.image,
            )
            favorite_dish.save()  
            return redirect('MyFavoriteDishes:show_favorite')  
    else:
        form = FavoriteDishFromCatalogueForm()

    foods = Food.objects.all() 
    return render(request, 'add_favorite.html', {'form': form, 'foods': foods})

def add_favorite_dish(request):
    if request.method == 'POST':
        form = FavoriteDishForm(request.POST)
        if form.is_valid():
            favorite_dish = form.save(commit=False)
            favorite_dish.user = request.user
            favorite_dish.save()
            return redirect('MyFavoriteDishes:show_favorite') 
    else:
        form = FavoriteDishForm()
    return render(request, 'add_favorite_dish.html', {'form': form})

...
@csrf_exempt
@require_POST
def add_fav_dish_ajax(request):
    name = request.POST.get("name")
    flavor = request.POST.get("flavor")
    category = request.POST.get("category")
    vendor_name = request.POST.get("vendor_name") 
    price = request.POST.get("price")
    map_link = request.POST.get("map_link")
    address = request.POST.get("address")
    user = request.user

    new_fav_dish = FavoriteDish(
        name=name, flavor=flavor,
        category=category, vendor_name=vendor_name,
        price=price, map_link=map_link, address=address,
        user=user
    )
    new_fav_dish.save()

    return HttpResponse(b"CREATED", status=201)

def edit_favorite_dish(request, uuid):
    favorite_dish = FavoriteDish.objects.get(pk = uuid)
    form = FavoriteDishForm(request.POST or None, instance=favorite_dish)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('MyFavoriteDishes:show_favorite'))

    context = {'form': form}
    return render(request, "edit_favorite_dish.html", context)

def delete_favorite_dish(request, uuid):
    favorite_dish = FavoriteDish.objects.get(pk = uuid)
    favorite_dish.delete()  # Remove from favorites
    return HttpResponseRedirect(reverse('MyFavoriteDishes:show_favorite'))

def show_json(request):
    favorite_dishes = FavoriteDish.objects.filter(user=request.user)

    flavor_filter = request.GET.get('flavor')
    category_filter = request.GET.get('category')
    name_filter = request.GET.get('name')

    if flavor_filter:
        favorite_dishes = favorite_dishes.filter(flavor__icontains=flavor_filter)
    if category_filter:
        favorite_dishes = favorite_dishes.filter(category__iexact=category_filter)
    if name_filter:
        favorite_dishes = favorite_dishes.filter(name__icontains=name_filter)

    data = serializers.serialize("json", favorite_dishes)
    return HttpResponse(data, content_type="application/json")
