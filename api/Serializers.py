from rest_framework import serializers
from api.models import *
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    entries = serializers.IntegerField( source='entries.count', read_only=True)
    class Meta:
        model = Task
        fields = ('id', 'title' ,'severity' ,'hostname', 'ip_address', 'publication_date','entries')

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username' ,'email' ,'status')
    
