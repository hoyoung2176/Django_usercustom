from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
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
    return render(request, 'accounts/auth_form.html', context)

# 함수 이름이랑 import 한 것이랑 같으므로, import 한 것을 이름 바꾼다.
def login(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.POST.get('next') or 'boards:index')
        
            
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
        'next' : request.GET.get('next', ''),
    }
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
    return render(request, 'accounts/auth_form.html', context)
    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)   # 인자 순서 유의
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 현재 유저가 로그아웃 되는 것을 막아준다. 세션 무효화 되는것을 막는다.
            return redirect('boards:index')
            
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form,}
    return render(request, 'accounts/auth_form.html', context)