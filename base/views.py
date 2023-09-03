from django.shortcuts import render ,redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate , login, logout
from django.contrib import messages #To throw in messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q #Allows Relational operations.
from .models import Room ,Topic , Message #Room refers to the model name(class name).
from .forms import RoomForm #importing from form.py file


# Create your views here.

# rooms = [
#     {'id':1 ,'name':'Lets Learn Python!'},
#     {'id':2 ,'name':'Design With Me'},
#     {'id':3 ,'name':'Frontend Developer'},

# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    #Checks whether user exits else throws error message
    if request.method=="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request , 'user does not exist')
        #authenticate checks for username and pass if it exits in the db if true, then sets the user
        user = authenticate(request , username=username , password=password)
        if user is not None:
            login(request , user)
            return redirect('home')
        else:
            messages.error(request , "Username or Password does not exist")
        
            
    context = {'page':page}
    return render(request , 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username  = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request , "An error occured during registration.")

    return render(request , 'base/login_register.html',{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains =q) |
                                Q(description__icontains=q)
                                  )#filter: filters out the data based on conditions.
    #Takes in all data(rooms in the database) from Room model/class.
    #We can also use .get(), .filter(), .exclude() do get specified objects/data.


    topics = Topic.objects.all()
    room_count = rooms.count() #we can also use len(rooms) 
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))


    context = {'rooms': rooms, 'topics':topics , 'room_count':room_count , 'room_messages':room_messages}
    return render(request , 'base/home.html',context) #render takes in the request from the server and access the templates that is required


def room(request, pk):
    room = Room.objects.get(id=pk) #Returns the room of the specified id
    room_messages = room.message_set.all()#set of messages related to a particular room(Messages Class).
    participants = room.participants.all()

    if request.method=="POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user) #User will added to many to many field.
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages':room_messages, 'participants': participants} #When the link is clicked the room associated with it is displayed on the window
    return render(request, "base/room.html", context) #Displays the templates on the browser window.

def userProfile(request ,pk):
    user = User.objects.get(id = pk)
    rooms=  user.room_set.all()
    room_messages = user.message_set.all() 
    topics  = Topic.objects.all()
    context = {'user':user , 'rooms':rooms ,'room_messages':room_messages, 'topics':topics,}
    return render(request , 'base/profile.html', context)



@login_required(login_url='login') #decorator allows only logged in users to create rooms(crud).
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') #Once the form is sumited the user is redirected to the home page.

    context = {'form':form}
    return render(request , 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request , pk):
    room = Room.objects.get(id= pk)
    form = RoomForm(instance=room)
    if request.user !=room.host:
        return HttpResponse("You can only update your rooms!")
    if request.method=='POST':
        form = RoomForm(request.POST, instance=room) #Only updates(edits) the  data of the given form instead of creating a new room.
        if form.is_valid():
            form.save()
            return redirect('home')
        
        

    context = {'form':form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method=="POST":
        room.delete()
        return redirect('home')
    if request.user!=room.host:
        return HttpResponse("You can only delete your room.")
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    room = Room.objects.get(id=pk) 
    if request.user!=message.user:
        return HttpResponse("You can only delete your message.")
    if request.method=="POST":
        message.delete()
        return redirect('room' , pk = room.id)
  
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def deleteMessageActivity(request, pk):
    message = Message.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse("You can only delete your message.")
    if request.method=="POST":
        message.delete()
        return redirect('home')
  
    return render(request, 'base/delete.html', {'obj':message}) 