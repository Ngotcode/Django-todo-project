from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone

# Create your views here.
def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':

        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
         #create a new user
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')

            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has been taken.  Please choose new username.'})
        else:
            #print("hello")   #Tell the user the passwords didn't match in the sigupuser.html page
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match.'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
        
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')


def logoutuser(request):
    if request.method == 'POST':
       # pass
       logout(request)
       return redirect('home')

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)        #so that it won't save in the database
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
            #pass
        except ValueError:        #if name title too long for example
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})

def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    #todos: Todo.objects.all()        #this list todos for all users
    return render(request, 'todo/currenttodos.html', {'todos':todos})

def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)     #pass in Todo clas, and pk-primary key
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)    #instance tells it is an existing object and trying to update it
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad Info'})
 
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)     #pass in Todo clas, and pk-primary key
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)     #pass in Todo clas, and pk-primary key
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.delete()
        return redirect('currenttodos')