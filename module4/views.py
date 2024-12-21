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
                new_dish.status = NewDish.APPROVED  #admin langsung approve
            else:
                new_dish.status = NewDish.PENDING  #pending kalo bukan admin
            
            new_dish.save()

            if new_dish.status == NewDish.APPROVED:
                create_food_entry(new_dish)
                messages.success(request, 'Dish added and approved successfully!')
            else:
                messages.success(request, 'Dish added successfully! Please wait for our admin to approve it.')
            
            return redirect('module4:add_dish')
            
    context = {"form": form}
    return render(request, 'add_dish.html', context)

@login_required
def check_dish(request):
    if not request.user.is_admin:
        return redirect('main:show_main')

    pending_dishes = NewDish.objects.filter(status=NewDish.PENDING)
    context = {'pending_dishes': pending_dishes}
    return render(request, 'check_dish.html', context)

@require_http_methods(["POST"])
def approve_dish(request, dish_uuid):
    if not request.user.is_admin:
        return JsonResponse({'success': False, 'status': 'forbidden'}, status=403)

    dish = get_object_or_404(NewDish, uuid=dish_uuid)
    
    try:
        data = json.loads(request.body)
        action = data.get('action')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'status': 'error', 'message': 'Invalid JSON'}, status=400)

    if action == 'approve':
        dish.status = NewDish.APPROVED
        dish.is_approved = True
        dish.save()
        create_food_entry(dish)
        return JsonResponse({'success': True, 'status': 'approved'})
    
    elif action == 'reject':
        dish.status = NewDish.REJECTED
        dish.is_rejected = True
        dish.save()
        return JsonResponse({'success': True, 'status': 'rejected'})

    return JsonResponse({'success': False, 'status': 'error', 'message': 'Invalid action'}, status=400)

#gadipake
@login_required
def edit_rejected_dish(request, dish_uuid):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            dish = NewDish.objects.get(uuid=dish_uuid)
            dish.name = data['name']
            dish.flavor = data['flavor']
            dish.category = data['category']
            dish.price = data['price']
            dish.map_link = data['map_link']
            dish.address = data['address']
            dish.image = data['image']
            dish.save()
            return JsonResponse({'message': 'Dish updated successfully'}, status=200)
        except NewDish.DoesNotExist:
            return JsonResponse({'error': 'Dish not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def create_food_entry(dish):
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
    if not request.user.is_authenticated:
        print("User is not authenticated, redirecting to login...")
        return redirect('login')

    pending_dishes = NewDish.objects.filter(user=request.user)

    print(f"Found {len(pending_dishes)} pending dishes for user {request.user.username}")

    return render(request, 'request_status_page.html', {
        'pending_dishes': pending_dishes
    })
    
@login_required
@csrf_exempt
def delete_dish(request, dish_uuid):
    print(f"Deleting dish with UUID: {dish_uuid}")
    if request.method == 'DELETE':
        print (f"Deleting dish with UUID: {dish_uuid}")
        dish = get_object_or_404(NewDish, uuid=dish_uuid)
        
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
    dish = get_object_or_404(NewDish, uuid=dish_uuid)

    if dish.status != NewDish.REJECTED:
        return JsonResponse({"error": "Only rejected dishes can be edited."}, status=400)

    if request.method == 'POST':
        try:
            # Load data dari request body
            data = json.loads(request.body)

            dish.name = data.get('name', dish.name)
            dish.flavor = data.get('flavor', dish.flavor)
            dish.category = data.get('category', dish.category)
            dish.price = data.get('price', dish.price)
            dish.map_link = data.get('map_link', dish.map_link)
            dish.address = data.get('address', dish.address)
            dish.image = data.get('image', dish.image)

            dish.status = NewDish.PENDING
            dish.is_approved = False
            dish.is_rejected = False

            dish.save()

            return JsonResponse({"message": "Dish updated and is now pending approval!"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)

def show_json(request):
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
        'user__username'
    )

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
            if request.user.is_admin:
                new_dish.status = NewDish.APPROVED
            else:
                new_dish.status = NewDish.PENDING
            
            new_dish.save()

            if new_dish.status == NewDish.APPROVED:
                create_food_entry(new_dish)
                return JsonResponse({'success': True, 'status': 'success', 'message': 'Dish added and approved successfully!'}, status=201)
            else:
                return JsonResponse({'success': True, 'status': 'success', 'message': 'Dish added successfully! Please wait for our admin to approve it.'}, status=201)
        else:
            return JsonResponse({'success': False, 'status': 'error', 'message': form.errors}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

@csrf_exempt
@login_required
def flutter_edit_rejected_dish(request, dish_uuid):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        dish = get_object_or_404(NewDish, uuid=dish_uuid)

        if dish.status != NewDish.REJECTED:
            return JsonResponse({'success': False, 'error': 'Only rejected dishes can be edited.'}, status=403)

        form = NewDishForm(data, instance=dish)
        if form.is_valid():
            updated_dish = form.save(commit=False)
            updated_dish.status = NewDish.PENDING
            updated_dish.is_approved = False
            updated_dish.is_rejected = False
            updated_dish.save()
            return JsonResponse({'success': True, 'message': 'Dish updated successfully!'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': form.errors}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

@csrf_exempt
@login_required
def flutter_delete_rejected_dish(request, dish_uuid):
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        dish = get_object_or_404(NewDish, uuid=dish_uuid)
        if dish.status != NewDish.REJECTED:
            return JsonResponse({'success': False, 'error': 'Only rejected dishes can be deleted.'}, status=403)
        dish.delete()
        return JsonResponse({'success': True, 'status': 'success', 'message': 'Dish deleted successfully!'}, status=200)

    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

@csrf_exempt
@login_required
def flutter_get_pending_dishes(request):
    if not request.user.is_admin:
        return JsonResponse({'success': False, 'status': 'forbidden', 'message': 'You are not authorized to approve dishes.'}, status=403)
    
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
        'is_approved',
        'is_rejected',
        'status',
        'user__username'
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

@csrf_exempt
@login_required
def flutter_approve_dish(request, dish_uuid):
    if not request.user.is_admin:
        return JsonResponse({'success': False, 'status': 'forbidden', 'message': 'You are not authorized to approve dishes.'}, status=403)

    dish = get_object_or_404(NewDish, uuid=dish_uuid)

    try:
        data = json.loads(request.body)
        action = data.get('action')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'status': 'error', 'message': 'Invalid JSON'}, status=400)

    if action == 'approve':
        dish.status = NewDish.APPROVED
        dish.is_approved = True
        dish.is_rejected = False
        dish.save()
        create_food_entry(dish)
        return JsonResponse({'success': True, 'status': 'approved', 'message': 'Dish approved successfully!'}, status=200)

    elif action == 'reject':
        dish.status = NewDish.REJECTED
        dish.is_approved = False
        dish.is_rejected = True
        dish.save()
        return JsonResponse({'success': True, 'status': 'rejected', 'message': 'Dish rejected successfully!'}, status=200)

    return JsonResponse({'success': False, 'status': 'error', 'message': 'Invalid action'}, status=400)
