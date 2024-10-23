from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
# Fungsi untuk menghubungkan user ke landing page berdasarkan usernya
def show_main(request):
    # if request.user.is_authenticated():
    #     context = {
    #         'name' : request.user.username
    #     }
    #     return render(request, 'logged_in_main.html', context)
    # else:
    return render(request, 'guest_main.html')

# Fitur login
def register(request):  
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)