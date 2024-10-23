from django.shortcuts import render, redirect
from module4.models import NewDish
from module4.forms import NewDishForm
from django.shortcuts import get_object_or_404

# Create your views here.
def show_home(request):
    # Tampilkan hanya dish yang sudah di-approve
    approved_dishes = NewDish.objects.filter(is_approved=True)
    return render(request, 'home.html', {'dishes': approved_dishes})

def add_dish(request):
    form = NewDishForm(request.POST, request.FILES or None)
    if form.is_valid() and request.method == 'POST':
        new_dish = form.save(commit=False)
        new_dish.user = request.user
        
        # Jika admin, dish langsung di-approve
        if request.user.is_staff:  # Django default check for admin (staff)
            new_dish.is_approved = True
            new_dish.save()
            return redirect('module4:show_home')  # Redirect ke home setelah approve
        else:
            # Jika user, dish belum di-approve dan disimpan untuk dicek oleh admin
            new_dish.is_approved = False
            new_dish.save()
            return redirect('module4:show_home')  # Redirect ke halaman cek_dish
    
    context = {"form": form}
    return render(request, 'add_dish.html', context)

def check_dish(request):
    if not request.user.is_staff:
        return redirect('module4:show_home')  # Hanya admin yang bisa mengakses halaman ini

    # Tampilkan dish yang belum di-approve
    pending_dishes = NewDish.objects.filter(is_approved=False)
    context = {'pending_dishes': pending_dishes}
    return render(request, 'check_dish.html', context)

def approve_dish(request, dish_id):
    if not request.user.is_staff:
        return redirect('module4:show_home')  # Hanya admin yang bisa melakukan ini

    dish = get_object_or_404(NewDish, id=dish_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            dish.is_approved = True
            dish.save()  # Approve dish
        elif action == 'delete':
            dish.delete()  # Hapus dish

    return redirect('module4:check_dish')  # Kembali ke halaman cek setelah aksi