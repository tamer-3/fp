from email import message
from pydoc_data.topics import topics
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Message, Room, Topic
from .forms import RoomForm

def about(request):
    aabout = True
    return render(request, 'base/about.html', {})

def loginpage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
           messages.error(request, 'Name or Password are incorrect')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'base/login.html', {'page':page})

def log_out(request):
    logout(request)
    return redirect('home')

def registration(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    return render(request, 'base/login.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q)|
        Q(name__icontains = q)|
        Q(decription__icontains = q)
        )

    topics = Topic.objects.all()
    rooms_count = rooms.count()
    comment_messages = Message.objects.all()
    return render(request, 'base/home.html', {'rooms':rooms, 'topics':topics,
    'rooms_count':rooms_count, 'comment_messages':comment_messages })

def room(request, pk):
    room = Room.objects.get(id=pk)
    comment_messages = room.message_set.all().order_by('-created')

    if request.method == "POST":
        message == Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('room', pk = room.id)

    return render(request, 'base/room.html', {'room':room, 'comment_messages':comment_messages})

def user_profile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    return render(request, 'base/profile.html', {'user': user, 'rooms': rooms,
    'topics': topics})

@login_required(login_url='/login')
def createroom(request):
    form = RoomForm()

    if request.method == "POST":
        form  = RoomForm(request.POST)
        
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    return render(request, 'base/room_form.html', {'form':form})

@login_required(login_url='/login')
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form  = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/room_form.html', {'form':form})

@login_required(login_url='/login')
def delroom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})
