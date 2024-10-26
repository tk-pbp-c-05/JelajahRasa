from django.shortcuts import render
from main.models import Food

def view_catalog(request):
    catalogs = Food.objects.all
    context = {
        'catalogs' : catalogs
    }
    return render(request, 'catalog.html', context)

