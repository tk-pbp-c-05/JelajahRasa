# MyFavoriteDishes/views.py

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from .models import Food, FavoriteDish
from .forms import FavoriteDishForm
from .forms import FavoriteDishFromCatalogueForm

def view_favorite_dishes(request):
    favorite_dishes = FavoriteDish.objects.all() # Fetch all favorite dishes
    return render(request, 'view_favorite_dishes.html', {'favorite_dishes': favorite_dishes})

def add_favorite(request):
    if request.method == 'POST':
        form = FavoriteDishFromCatalogueForm(request.POST)
        if form.is_valid():
            food = form.cleaned_data['food']  # Get the selected Food instance
            # Create a new FavoriteDish instance with details from the selected Food
            favorite_dish = FavoriteDish(
                food=food,
                name=food.name,  # Use the name of the selected Food
                flavor=food.flavor,
                category="Makanan",  # Or dynamically set if you have category data
                vendor_name=food.vendor_name,  # Use the vendor name from the Food instance
                price=food.price,  # Use the price from the Food instance
                map_link=food.map_link,  # Use the map link from the Food instance
                address=food.address  # Use the address from the Food instance
            )
            favorite_dish.save()  # Save the new favorite dish to the database
            return redirect('MyFavoriteDishes:view_favorite_dishes')  # Redirect to the favorites page
    else:
        form = FavoriteDishFromCatalogueForm()

    foods = Food.objects.all()  # Get all food items for the dropdown
    return render(request, 'add_favorite.html', {'form': form, 'foods': foods})

def add_favorite_dish(request):
    if request.method == 'POST':
        form = FavoriteDishForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new favorite dish
            return redirect('MyFavoriteDishes:view_favorite_dishes')  # Redirect to view page
    else:
        form = FavoriteDishForm()
    return render(request, 'add_favorite_dish.html', {'form': form})

def edit_favorite_dish(request, id):
    # Get favorite dish entry by id
    favorite_dish = FavoriteDish.objects.get(pk = id)

    # Set favorite dish entry as an instance of the form
    form = FavoriteDishForm(request.POST or None, instance=favorite_dish)

    if form.is_valid() and request.method == "POST":
        # Save form and return to the main page
        form.save()
        return HttpResponseRedirect(reverse('MyFavoriteDishes:view_favorite_dishes'))

    context = {'form': form}
    return render(request, "edit_favorite_dish.html", context)

def delete_favorite_dish(request, id):
    favorite_dish = FavoriteDish.objects.get(pk = id)
    # Hapus mood
    favorite_dish.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('MyFavoriteDishes:view_favorite_dishes'))

