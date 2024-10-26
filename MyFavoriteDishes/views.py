# MyFavoriteDishes/views.py

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect, JsonResponse
from .models import Food, FavoriteDish
from .forms import FavoriteDishForm
from .forms import FavoriteDishFromCatalogueForm

def show_favorite(request):
    favorite_dishes = FavoriteDish.objects.filter(user=request.user) 
    return render(request, 'show_favorite.html', {'favorite_dishes': favorite_dishes})

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
                category="Makanan",  
                vendor_name=food.vendor_name,  
                price=food.price,  
                map_link=food.map_link,  
                address=food.address  
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

def edit_favorite_dish(request, uuid):
    favorite_dish = FavoriteDish.objects.get(pk = uuid)
    form = FavoriteDishForm(request.POST or None, instance=favorite_dish)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('MyFavoriteDishes:show_favorite'))

    context = {'form': form}
    return render(request, "edit_favorite_dish.html", context)

def delete_favorite_dish(request, uuid):
    #favorite_dish = FavoriteDish.objects.get(pk = id)
    favorite_dish = get_object_or_404(FavoriteDish, user=request.user, uuid=uuid)
    favorite_dish.delete()  # Remove from favorites

    return JsonResponse({'status': 'removed', 'is_favorite': False})