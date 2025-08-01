from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import User

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Check if user needs verification
            if user.is_verified:
                messages.success(request, 'Registration successful! You can now access the dashboard.')
            else:
                messages.success(request, 'Registration successful! Please wait for admin approval before you can access all features.')
            login(request, user)
            return redirect('dashboard:home')
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def user_list(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard:home')
    
    # Filter users by society if user is society admin
    if request.user.society:
        users = User.objects.filter(society=request.user.society).order_by('wing', 'flat_number')
    else:
        users = User.objects.all().order_by('wing', 'flat_number')
        
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
def verify_user(request, user_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard:home')
    
    try:
        user = User.objects.get(id=user_id)
        user.is_verified = not user.is_verified
        user.save()
        status = 'verified' if user.is_verified else 'unverified'
        messages.success(request, f'User {user.username} has been {status}!')
    except User.DoesNotExist:
        messages.error(request, 'User not found!')
    
    return redirect('accounts:user_list')