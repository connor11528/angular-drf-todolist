from django.shortcuts import render
from rest_framework import viewsets

from jsframework.models import Todo
from serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer

def index(request):
    return render(request, 'jsframework/base.html')