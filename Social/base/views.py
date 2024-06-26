from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm




def loginPage(request):
    """This view is related to user login."""

    page='login'
    if request.user.is_authenticated:
        return redirect('base:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist!', 'danger')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'User Logged In.', 'success')
            return redirect('base:home')
        else:
            messages.error(request, 'Username or Password Is Wrong!', 'danger')

    context={'page':page}
    return render(request, 'base/login_register.html', context)



def logoutUser(request):
    """This view is related to user logout."""

    logout(request)
    return redirect('base:home')



def registerPage(request):
    """This view is related to user register."""

    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'You Register successfully.', 'success')
            return redirect('base:home')
        else:
            messages.error(request, 'An error occured during registration!', 'danger')
    context= {'form':form}
    return render(request, 'base/login_register.html', context)



def home(request):
    """This view is related to main page and search"""

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 'topics':topics, 
            'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)




def room(request, pk):
    """This view is related to room in main page."""

    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('base:room', pk=room.id)
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)




def userProfile(request, pk):
    """This view is related to user profile."""

    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user, 'rooms':rooms, 'room_messages':room_messages, 
            'topics':topics}
    return render(request, 'base/profile.html', context)




@login_required(login_url='login')
def roomcreate(request):
    """This view is related to building the room that is shown on the main page."""

    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('base:home')
    context={'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)




@login_required(login_url='login')
def updateroom(request, pk):
    """This view is about updating the room we created earlier and update topics. """

    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You can't access this page!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('base:home')
    
    context={'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')
def deleteroom(request, pk):
    """This view is related to deleting the room we created earlier."""

    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You can't access this page!")
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'you deleted room successfully', 'success')
        return redirect('base:home')
    return render(request, 'base/delete.html', {'obj':room})



@login_required(login_url='login')
def deleteMessage(request, pk):
    """
    This view is related to deleting the message 
    that the user leaves on the created room.
    """

    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You can't delete...")
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'you deleted message successfully', 'success')
        return redirect('base:home')
    return render(request, 'base/delete.html', {'obj':message})



@login_required(login_url='login')
def updateuser(request):
    """This view is related to updating the profile of a registered user."""

    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('base:user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form':form})




def topicsPage(request):
    """
    write the name of the topic in it, the name of that room becomes our topic, and this 
    view shows the name of the room topic that we created before when creating the room.
    """

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})



def activityPage(request):
    """
    This view is related to Recent activities 
    which is on the right side of the main page
    """

    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})