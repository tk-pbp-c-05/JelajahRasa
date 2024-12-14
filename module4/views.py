from django.shortcuts import render, redirect, get_object_or_404
from module4.models import NewDish
from main.models import Food
from module4.forms import NewDishForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

# Tampilkan home dengan hanya dish yang sudah di-approve
def show_home(request):
    approved_dishes = NewDish.objects.filter(status=NewDish.APPROVED)
    return render(request, 'home.html', {'dishes': approved_dishes})

# Form untuk menambahkan dish
@login_required
def add_dish(request):
    form = NewDishForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            new_dish = form.save(commit=False)
            new_dish.user = request.user
            
            if request.user.is_admin:
                new_dish.status = NewDish.APPROVED  # Admin langsung approve
            else:
                new_dish.status = NewDish.PENDING  # Status pending jika bukan admin
            
            new_dish.save()

            # Cek apakah dish di-approve langsung atau perlu menunggu admin
            if new_dish.status == NewDish.APPROVED:
                create_food_entry(new_dish)  # Panggil fungsi untuk membuat entri di Food
                messages.success(request, 'Dish added and approved successfully!')
            else:
                messages.success(request, 'Dish added successfully! Please wait for our admin to approve it.')
            
            return redirect('module4:add_dish')  # Redirect ke halaman 'add_dish' setelah berhasil
            
    context = {"form": form}
    return render(request, 'add_dish.html', context)

# Menampilkan dish yang belum di-approve
@login_required
def check_dish(request):
    if not request.user.is_admin:
        return redirect('main:show_main')

    pending_dishes = NewDish.objects.filter(status=NewDish.PENDING)
    context = {'pending_dishes': pending_dishes}
    return render(request, 'check_dish.html', context)

# Fungsi untuk approve atau reject dish dengan AJAX
@require_http_methods(["POST"])
def approve_dish(request, dish_uuid):
    if not request.user.is_admin:
        return JsonResponse({'status': 'forbidden'}, status=403)

    dish = get_object_or_404(NewDish, uuid=dish_uuid)
    
    try:
        data = json.loads(request.body)
        action = data.get('action')
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    if action == 'approve':
        dish.status = NewDish.APPROVED
        dish.is_approved = True
        dish.save()
        create_food_entry(dish)
        return JsonResponse({'status': 'approved'})
    
    elif action == 'reject':
        dish.status = NewDish.REJECTED
        dish.is_rejected = True
        dish.save()
        return JsonResponse({'status': 'rejected'})

    return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)


# Fungsi untuk edit dish yang statusnya rejected
@login_required
def edit_rejected_dish(request, dish_uuid):
    # Cari dish berdasarkan UUID
    dish = get_object_or_404(NewDish, uuid=dish_uuid)

    if request.method == 'POST':
            uuid = request.POST.get('uuid')
            dish = NewDish.objects.get(uuid=uuid)
            dish.name = request.POST.get('name')
            dish.flavor = request.POST.get('flavor')
            dish.category = request.POST.get('category')
            dish.vendor_name = request.POST.get('vendor_name')
            dish.price = request.POST.get('price')
            dish.map_link = request.POST.get('map_link')
            dish.address = request.POST.get('address')
            dish.image = request.POST.get('image')

            dish.save()
            return redirect('module4:request_status')

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
        
@login_required
def request_status(request):
    # Pastikan user sudah login
    if not request.user.is_authenticated:
        print("User is not authenticated, redirecting to login...")
        return redirect('login')  # Ganti dengan URL login yang sesuai

    # Ambil daftar dish yang belum disetujui atau ditolak
    pending_dishes = NewDish.objects.filter(user=request.user)

    # Debug: Cek data pending_dishes yang didapatkan
    print(f"Found {len(pending_dishes)} pending dishes for user {request.user.username}")

    return render(request, 'request_status_page.html', {
        'pending_dishes': pending_dishes
    })
    
    # Fungsi untuk menghapus dish
@login_required
@csrf_exempt
def delete_dish(request, dish_uuid):
    print(f"Deleting dish with UUID: {dish_uuid}")
    if request.method == 'DELETE':
        # Cek apakah dish dengan UUID tersebut ada
        print (f"Deleting dish with UUID: {dish_uuid}")
        dish = get_object_or_404(NewDish, uuid=dish_uuid)
        
        # Hapus dish
        dish.delete()
        
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=405)

def get_dish_data(request, dish_uuid):
    try:
        dish = NewDish.objects.get(uuid=dish_uuid)
        dish_data = {
            'uuid': dish.uuid,
            'name': dish.name,
            'flavor': dish.flavor,
            'category': dish.category,
            'price': dish.price,
            'map_link': dish.map_link,
            'address': dish.address,
            'image': dish.image if dish.image else '',
        }
        return JsonResponse(dish_data)
    except NewDish.DoesNotExist:
        return JsonResponse({'error': 'Dish not found'}, status=404)
    
@login_required
def edit_dish(request, dish_uuid):
    # Cari dish berdasarkan UUID
    dish = get_object_or_404(NewDish, uuid=dish_uuid)

    # Pastikan hanya dish yang ditolak yang bisa diedit
    if dish.status != NewDish.REJECTED:
        messages.error(request, "Only rejected dishes can be edited.")
        return redirect('module4:request_status')

    # Proses form jika metode request POST
    if request.method == 'POST':
        form = NewDishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            updated_dish = form.save()

            # Jika dish diubah, update status menjadi 'Pending' untuk menunggu review ulang oleh admin
            updated_dish.status = NewDish.PENDING  # Ubah status menjadi Pending setelah edit
            updated_dish.is_approved = False  # Pastikan dish belum disetujui
            updated_dish.is_rejected = False  # Reset status rejection
            updated_dish.save()

            messages.success(request, "Dish updated and is now pending approval!")
            return redirect('module4:request_status')  # Redirect ke halaman request status
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NewDishForm(instance=dish)  # Menampilkan form dengan data dish yang sudah ada

    context = {
        "form": form,
        "dish": dish
    }
    return render(request, 'edit_dish.html', context)

def show_json(request):
    # Query all dishes
    dishes = NewDish.objects.all().values(
        'uuid',
        'name',
        'flavor',
        'category',
        'vendor_name',
        'price',
        'map_link',
        'address',
        'image',
        'is_approved',
        'is_rejected',
        'status',
        'user__username'  # Including the username of the user who added the dish
    )

    # Convert QuerySet to a list
    dish_list = list(dishes)
    
    return JsonResponse(dish_list, safe=False)

@csrf_exempt
@login_required
def flutter_add_dish(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = NewDishForm(data)
        if form.is_valid():
            new_dish = form.save(commit=False)
            new_dish.user = request.user
            new_dish.status = NewDish.PENDING  # Default status
            new_dish.save()
            return JsonResponse({'status': 'success', 'message': 'Dish added successfully!'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
@login_required
def flutter_edit_rejected_dish(request, dish_uuid):
    if request.method == 'PUT':
        dish = get_object_or_404(NewDish, uuid=dish_uuid)
        if dish.status != NewDish.REJECTED:
            return JsonResponse({'error': 'Only rejected dishes can be edited.'}, status=403)
        
        data = json.loads(request.body)
        form = NewDishForm(data, instance=dish)
        if form.is_valid():
            updated_dish = form.save(commit=False)
            updated_dish.status = NewDish.PENDING  # Update status to pending
            updated_dish.is_approved = False
            updated_dish.is_rejected = False
            updated_dish.save()
            return JsonResponse({'status': 'success', 'message': 'Dish updated successfully!'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
@login_required
def flutter_delete_rejected_dish(request, dish_uuid):
    if request.method == 'DELETE':
        dish = get_object_or_404(NewDish, uuid=dish_uuid)
        if dish.status != NewDish.REJECTED:
            return JsonResponse({'error': 'Only rejected dishes can be deleted.'}, status=403)
        dish.delete()
        return JsonResponse({'status': 'success', 'message': 'Dish deleted successfully!'}, status=200)
    return JsonResponse({'error': 'Invalid method'}, status=405)


@csrf_exempt
@login_required
def flutter_get_pending_dishes(request):
    pending_dishes = NewDish.objects.filter(status=NewDish.PENDING).values(
        'uuid',
        'name',
        'flavor',
        'category',
        'vendor_name',
        'price',
        'map_link',
        'address',
        'image',
        'status'
    )
    return JsonResponse(list(pending_dishes), safe=False, status=200)

def flutter_get_dish_detail(request, dish_uuid):
    dish = get_object_or_404(NewDish, uuid=dish_uuid)
    dish_data = {
        'uuid': dish.uuid,
        'name': dish.name,
        'flavor': dish.flavor,
        'category': dish.category,
        'vendor_name': dish.vendor_name,
        'price': dish.price,
        'map_link': dish.map_link,
        'address': dish.address,
        'image': dish.image.url if dish.image else '',
        'status': dish.status
    }
    return JsonResponse(dish_data, status=200)

@login_required
def flutter_get_user_dishes(request):
    user = request.user
    dishes = NewDish.objects.filter(user=user).values(
        'uuid',
        'name',
        'flavor',
        'category',
        'vendor_name',
        'price',
        'map_link',
        'address',
        'image',
        'is_approved',
        'is_rejected',
        'status',
        'user__username'
    )
    return JsonResponse(list(dishes), safe=False)
