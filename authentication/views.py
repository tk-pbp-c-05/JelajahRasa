from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import json

User = get_user_model() # untuk get user custom

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                response_data = {
                    "status": "success",
                    "message": "Successfully Logged In!",
                    "username": user.username,
                    "is_admin": user.is_staff  # Using is_staff instead of is_admin
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid credentials."
                })
        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON format"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    })


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            username = data['username']
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            password1 = data['password1']
            password2 = data['password2']
            admin_code = data.get('admin_code', '')
            
            # Cek matching password
            if password1 != password2:
                return JsonResponse({
                    "status": "error",
                    "message": "Passwords do not match."
                }, status=400)
            
            # Cek username sudah ada atau belum
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Username already exists."
                }, status=400)
                
            # Cek email sudah ada atau belum
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    "status": "error",
                    "message": "This email is already registered."
                }, status=400)

            # Buat user baru dengan custom user model
            user = User.objects.create_user(
                username=username,
                password=password1,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            
            # Cek admin code
            if admin_code == "PBPC05ASELOLE":
                user.is_staff = True
                user.is_superuser = True
            
            user.save()

            return JsonResponse({
                "username": user.username,
                "status": "success",
                "message": "User created successfully!"
            }, status=200)
            
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=400)

@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)