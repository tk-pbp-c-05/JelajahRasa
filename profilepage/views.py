from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import CustomUser

# Create your views here.

@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)
