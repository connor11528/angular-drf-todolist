from rest_framework import serializers
from jsframework.models import Todo

class TodoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Todo