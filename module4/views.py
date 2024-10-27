from django.shortcuts import render, redirect, get_object_or_404
from module4.models import NewDish
from main.models import Food
from module4.forms import NewDishForm
from django.http import JsonResponse
from django.contrib import messages

# Tampilkan home dengan hanya dish yang sudah di-approve
def show_home(request):
    approved_dishes = NewDish.objects.filter(is_approved=True)
    return render(request, 'home.html', {'dishes': approved_dishes})

# Form untuk menambahkan dish
def add_dish(request):
    form = NewDishForm(request.POST, request.FILES or None)
    if form.is_valid() and request.method == 'POST':
        new_dish = form.save(commit=False)
        new_dish.user = request.user
        
        if request.user.is_admin:
            new_dish.is_approved = True
        else:
            new_dish.is_approved = False
        
        new_dish.save()

        # Cek apakah dish di-approve langsung atau perlu menunggu admin
        if new_dish.is_approved:
            create_food_entry(new_dish)  # Panggil fungsi untuk membuat entri di Food
            messages.success(request, 'Dish added and approved successfully!')
        else:
            messages.success(request, 'Dish added successfully! Please wait for our admin to approve it.')
            
        return redirect('module4:add_dish')

    context = {"form": form}
    return render(request, 'add_dish.html', context)

# Menampilkan dish yang belum di-approve
def check_dish(request):
    if not request.user.is_admin:
        return redirect('module4:show_home')

    pending_dishes = NewDish.objects.filter(is_approved=False)
    context = {'pending_dishes': pending_dishes}
    return render(request, 'check_dish.html', context)

# Fungsi untuk approve atau delete dish dengan AJAX
def approve_dish(request, dish_uuid):
    print("Approve/Delete view called")
    if not request.user.is_admin:
        print("User not authorized")
        return JsonResponse({'status': 'forbidden'}, status=403)

    # Cari dish berdasarkan UUID
    dish = get_object_or_404(NewDish, uuid=dish_uuid)
    print(f"Dish found: {dish.name}")

    if request.method == 'POST':
        action = request.POST.get('action')
        print(f"Action received: {action}")
        
        # Jika action adalah approve
        if action == 'approve':
            dish.is_approved = True
            dish.save()
            print("Dish approved")
            create_food_entry(dish)  # Membuat entri di model Food
            return JsonResponse({'status': 'approved', 'dish_id': dish_uuid})
        
        # Jika action adalah delete
        elif action == 'delete':
            dish.delete()
            print("Dish deleted")
            return JsonResponse({'status': 'deleted', 'dish_id': dish_uuid})

    print("Invalid request method")
    return JsonResponse({'status': 'error'}, status=400)

# Fungsi untuk membuat entry di Food model ketika dish disetujui
def create_food_entry(dish):
    # Cek apakah sudah ada Food dengan UUID yang sama
    if not Food.objects.filter(uuid=dish.uuid).exists():
        Food.objects.create(
            uuid=dish.uuid,
            name=dish.name,
            flavor=dish.flavor,
            category=dish.category,
            vendor_name=dish.vendor_name,
            price=dish.price,
            map_link=dish.map_link,
            address=dish.address,
            image=dish.image
        )
        print(f"Food entry created for dish: {dish.name}")
    else:
        print(f"Food entry with UUID {dish.uuid} already exists.")
