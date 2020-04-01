from django.shortcuts import render

# Create your views here.
# chat/views.py
from django.shortcuts import render
from .consumers import ChatConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def sendDeployments():
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'chat_lobby',
        {'type': 'chat_message', 'message': 'tesst'}
    )


def index(request):
    
    sendDeployments()
    
    return render(request, 'chat/index.html')
    
def room(request, room_name):
    

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'msg_received' : "msg",
    })