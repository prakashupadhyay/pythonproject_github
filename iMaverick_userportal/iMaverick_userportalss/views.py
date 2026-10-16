from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from django.utils import timezone

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user =form.save()
            user_location = request.POST.get('location', '')
            UserProfile.objects.create(
                user=user,
                username=user.username,
                location=user_location,
                last_updated_by=user,  # Set initial updater to the user themselves
                signup_ip=request.META.get('REMOTE_ADDR')
            )
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please, You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the credentials match a stored user in the database
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)          


            profile = user.userprofile
            profile.last_login_at = timezone.now()
            profile.save(update_fields=['last_login_at'])
            return redirect('success')
        else:
            messages.error(request, 'Invalid Username or password.')
            return render(request, 'login.html')
            # return redirect('failure')
            
    return render(request, 'login.html')
@login_required
def success_view(request):
    # print("--- [GET /success/] UPON ARRIVAL ---")
    # print("Session ID:", request.session.session_key)
    # print("Session Data:", dict(request.session))
    return render(request, 'success.html', {'username': request.user.username})
    # username = request.session.get('logged_in_username', 'User')
    # return render(request, 'success.html', {'username': username})
    #return render(request, 'success.html')

def failure_view(request):
    username = request.GET.get('username', 'Unknown')
    return render(request, 'failure.html', {'username': username})