from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required


# Create your views here.


def signup(request):
    if request.method == "POST":
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')
        my_user = User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        return redirect('/loginn')
    return render(request, 'todo_app/signup.html')


def loginn(request):
    if request.method == "POST":
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        userr = authenticate(request, username = fnm, password = pwd)
        if userr is not None:
            login(request, userr)
            return redirect('/todopage')
        else:
            return redirect('/loginn')
    return render(request, 'todo_app/loginn.html')


@login_required(login_url='/loginn')
def todopage(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        task = models.Todo_DB(title=title, user=request.user)
        task.save()
        res = models.Todo_DB.objects.filter(user=request.user).order_by('-date')
        return redirect('/todopage', {'res': res})
    res = models.Todo_DB.objects.filter(user=request.user).order_by('-date')    
    return render(request, 'todo_app/todo.html', {'res': res})


@login_required(login_url='/loginn')
def edit_todo(request,srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        obj = models.Todo_DB.objects.get(srno=srno)
        obj.title = title
        obj.save()
        return redirect('/todopage')

    obj = models.Todo_DB.objects.get(srno=srno)
    return render(request, 'todo_app/edit_todo.html', {'obj': obj})


@login_required(login_url='/loginn')
def delete_todo(request,srno):
    obj = models.Todo_DB.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')


def signout(request):
    logout(request)
    return redirect('/loginn')