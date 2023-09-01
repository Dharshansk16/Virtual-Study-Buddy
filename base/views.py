from django.shortcuts import render ,redirect
from .models import Room #Room refers to the model name(class name).
from .forms import RoomForm #importing from form.py file


# Create your views here.

# rooms = [
#     {'id':1 ,'name':'Lets Learn Python!'},
#     {'id':2 ,'name':'Design With Me'},
#     {'id':3 ,'name':'Frontend Developer'},

# ]

def home(request):
    rooms = Room.objects.all() #Takes in all data(rooms in the database) from Room model/class.
    #We can also use .get(), .filter(), .exclude() do get specified objects/data.
    context = {'rooms': rooms}
    return render(request , 'base/home.html',context) #render takes in the request from the server and access the templates that is required


def room(request, pk):
    room = Room.objects.get(id=pk) #Returns the room of the specified id 
    context = {'room': room} #When the link is clicked the room associated with it is displayed on the window
    return render(request, "base/room.html", context) #Displays the templates on the browser window.


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') #Once the form is sumited the user is redirected to the home page.

    context = {'form':form}
    return render(request , 'base/room_form.html', context)


def updateRoom(request , pk):
    room = Room.objects.get(id= pk)
    form = RoomForm(instance=room)
    if request.method=='POST':
        form = RoomForm(request.POST, instance=room) #Only updates(edits) the  data of the given form instead of creating a new room.
        if form.is_valid():
            form.save()
            return redirect('home')
        

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method=="POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})