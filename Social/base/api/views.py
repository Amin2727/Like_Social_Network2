from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomsSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomsSerializer(rooms, many=True)
    return Response(serializer.data)




@api_view(['GET'])
def getRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    serializer = RoomsSerializer(room, many=False)
    return Response(serializer.data)