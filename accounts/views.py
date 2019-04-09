from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import UserCustomChangeForm

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('boards:index')
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request, 'accounts/signup.html', context)

# 함수 이름이랑 import 한 것이랑 같으므로, import 한 것을 이름 바꾼다.
def login(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('boards:index')
    else:
        form = AuthenticationForm()
    context = {'form' : form}
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('boards:index')
    
def delete(request):
    user = request.user
    if request.method == 'POST':
        #DELETE
        user.delete()
    return redirect('boards:index')

def edit(request):
    if request.method == 'POST':
        # 수정 로직 진행
        form = UserCustomChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('boards:index')
    else:
        form = UserCustomChangeForm(instance = request.user)
    context = {'form':form,}
    return render(request, 'accounts/edit.html', context)