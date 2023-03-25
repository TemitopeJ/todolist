from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Todo

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('manage')
        else:
            messages.info(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'login.html') 

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'This email already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'The password entered are not similar')
            return redirect('register')
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def manage(request):
    
    username = request.user

    account = User.objects.get(username=username)
    todolists = Todo.objects.filter(user=account)
    
    # todolists = Todo.objects.all()
    if request.method == 'POST':
        item = request.POST['todo-item']

        user = User.objects.get(username= username)
        todo = Todo.objects.create(user=user, title=item)
        todo.save()
        return redirect('manage')
        

    return render(request, 'manage.html', {'todolists': todolists})

def delete(request, num):
    todo = Todo.objects.get(id=num)
    todo.delete()
    return redirect('manage')

    