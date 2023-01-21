from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import  PostModelSerializer
from ..models import baza_ogloszen

@api_view(['GET','POST'])
def ogl_list(request):
    if request.method == 'GET':
        qs = baza_ogloszen.objects.all()
        serializer = PostModelSerializer(qs,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostModelSerializer(data = request.data)
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)