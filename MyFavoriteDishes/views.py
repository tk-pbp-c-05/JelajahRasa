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
import json
from django.http import JsonResponse


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

# def edit_favorite_dish(request, uuid):
#     favorite_dish = FavoriteDish.objects.get(pk = uuid)
#     form = FavoriteDishForm(request.POST or None, instance=favorite_dish)

#     if form.is_valid() and request.method == "POST":
#         form.save()
#         return HttpResponseRedirect(reverse('MyFavoriteDishes:show_favorite'))

#     context = {'form': form}
#     return render(request, "edit_favorite_dish.html", context)

def edit_favorite_dish(request, uuid):
    favorite_dish = get_object_or_404(FavoriteDish, pk=uuid)
    if favorite_dish.food is not None:
        return redirect(reverse('MyFavoriteDishes:show_favorite'))  
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

def show_json_flutter(request):
    data = FavoriteDish.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def add_favdish_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_favdish = FavoriteDish.objects.create(
            user=request.user,
            name=data["name"],
            price=int(data["price"]),
            image=data["image"],
            vendor_name=data["vendor_name"],
            flavor=data["flavor"],
            address=data["address"],
            category=data["category"],
            map_link=data["map_link"],
        )
        new_favdish.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)@csrf_exempt
    

@csrf_exempt
def delete_favorite_dish_flutter(request, uuid):
    if request.method == "POST":  # Gunakan POST untuk menggantikan DELETE
        dish = get_object_or_404(FavoriteDish, pk=uuid, user=request.user)
        dish.delete()
        return JsonResponse({"status": True, "message": "Favorite Dish deleted successfully."})
    return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def edit_favdish_flutter(request, uuid):
    if request.method == 'POST':
        data = json.loads(request.body)
        dish = get_object_or_404(FavoriteDish, pk=uuid, user=request.user)

        dish.name = data.get('name', dish.name)
        dish.price = int(data.get('price', dish.price))
        dish.image = data.get('image', dish.image)
        dish.vendor_name = data.get('vendor_name', dish.vendor_name)
        dish.flavor = data.get('flavor', dish.flavor)
        dish.address = data.get('address', dish.address)
        dish.category = data.get('category', dish.category)
        dish.map_link = data.get('map_link', dish.map_link)

        dish.save()
        return JsonResponse({"status": "success", "message": "Favorite dish updated successfully."})
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

def get_foodlist_flutter(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


@csrf_exempt
def select_favdish_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            food_id = data.get('pk') 
            if not food_id:
                return JsonResponse({"status": "error", "message": "Food ID is required"}, status=400)
            try:
                food = Food.objects.get(pk=food_id)
            except Food.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Food not found"}, status=404)
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)

            FavoriteDish.objects.create(
                user=user,
                food=food,
                name=food.name,  
                price=food.price,
                image=food.image,
                vendor_name=food.vendor_name,
                flavor=str(food.flavor),  
                address=food.address,
                category=str(food.category), 
                map_link=food.map_link,
            )
            return JsonResponse({"status": "success", "message": "Favorite dish added successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
    
    # Invalid request method
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)