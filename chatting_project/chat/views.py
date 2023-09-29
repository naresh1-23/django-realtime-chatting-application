from django.shortcuts import render, redirect
from user.models import User
from .models  import Chat, Room
from django.db.models import Q


# Create your views here.
def home(request, pk):
    user = request.user
    user_rooms = Room.objects.filter(Q(user1 = user.username) | Q(user2 = user.username))
    room = Room.objects.filter(id = pk).first()
    chats = Chat.objects.filter(room = room)
    return render(request, 'chat/home.html', {'pk': pk, 'user': user, 'room': room, "user_rooms": user_rooms, "chats": chats})



def mainHome(request):
    user = request.user
    user_rooms = Room.objects.filter(user1 = user.username) | Room.objects.filter(user2 = user.username)
    return render(request, "chat/mainhome.html", {"user_rooms": user_rooms})



def CheckRoom(request, pk):
    user = User.objects.filter(id = pk).first()
    print(user)
    room = Room.objects.filter(Q(user1 = user.username, user2 = request.user.username) | Q(user1= request.user.username , user2 = user.username)).first()
    if room:
        print("already")
        return redirect("chat-home", pk = room.id)
    else:
        if user.username == request.user.username:
            return redirect("home")
        new_room = Room.objects.create(user1 = user.username, user2 = request.user.username)
        new_room.save()
        return redirect("chat-home", pk = new_room.id)
    
    
    
def Search(request, q):
    if len(q)>3:
        users = User.objects.filter(username__icontains = q) and User.objects.exclude(username = request.user.username)    
        return render(request, "chat/data.html", {'users': users})
    