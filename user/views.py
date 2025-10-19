from django.contrib import auth
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render, redirect
from .forms import UserForm

# Create your views here.

def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return render(request, 'user/success.html')
        else:
            return render(request, 'user/sign_up_form.html', {'form': form})
    else:
        form = UserForm()
    return render(request, 'user/sign_up_form.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def mypage_view(request):
    return render(request, 'user/mypage.html')

# def log_in(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#     else:
#         return render(request, 'user/login.html')