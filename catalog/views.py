from django.shortcuts import render
from main.models import Food

def view_catalog(request):
    # Ambil semua objek Food
    catalogs = Food.objects.all()
    
    # Filter berdasarkan flavor (rasa)
    flavor = request.GET.get('flavor')  # 'salty' atau 'sweet'
    if flavor:
        catalogs = catalogs.filter(flavor=flavor)

    # Filter berdasarkan type (jenis)
    type_ = request.GET.get('type')  # 'beverage' atau 'food'
    if type_:
        catalogs = catalogs.filter(type=type_)

    # Sorting berdasarkan harga atau nama, dan urutan ascend/descend
    sort_by = request.GET.get('sort_by')  # 'price' atau 'name'
    order = request.GET.get('order')  # 'asc' untuk ascend atau 'desc' untuk descend
    
    if sort_by in ['price', 'name']:
        if order == 'desc':
            catalogs = catalogs.order_by(f'-{sort_by}')  # Descending order
        else:
            catalogs = catalogs.order_by(sort_by)  # Ascending order (default)

    context = {
        'catalogs': catalogs,
    }
    return render(request, 'catalog.html', context)
