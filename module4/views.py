from django.shortcuts import render, redirect, get_object_or_404
from module4.models import NewDish
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
        
        if request.user.is_superuser:
            new_dish.is_approved = True
            new_dish.save()
            messages.success(request, 'Dish added successfully!')
            return redirect('module4:show_home')  # Redirect ke home setelah approve
        else:
            new_dish.is_approved = False
            new_dish.save()
            messages.success(request, 'Dish added successfully! Please wait for our admin to approve it.')
            return redirect('module4:show_home')
    
    context = {"form": form}
    return render(request, 'add_dish.html', context)

# Menampilkan dish yang belum di-approve
def check_dish(request):
    if not request.user.is_staff:
        return redirect('module4:show_home')  # Hanya admin yang bisa mengakses halaman ini

    pending_dishes = NewDish.objects.filter(is_approved=False)
    context = {'pending_dishes': pending_dishes}
    return render(request, 'check_dish.html', context)

# Fungsi untuk approve atau delete dish dengan AJAX
def approve_dish(request, dish_id):
    print("Approve/Delete view called")
    if not request.user.is_staff:
        print("User not authorized")
        return JsonResponse({'status': 'forbidden'}, status=403)

    dish = get_object_or_404(NewDish, id=dish_id)
    print(f"Dish found: {dish.name}")

    if request.method == 'POST':
        action = request.POST.get('action')
        print(f"Action received: {action}")
        if action == 'approve':
            dish.is_approved = True
            dish.save()
            print("Dish approved")
            return JsonResponse({'status': 'approved', 'dish_id': dish_id})
        elif action == 'delete':
            dish.delete()
            print("Dish deleted")
            return JsonResponse({'status': 'deleted', 'dish_id': dish_id})

    print("Invalid request method")
    return JsonResponse({'status': 'error'}, status=400)
