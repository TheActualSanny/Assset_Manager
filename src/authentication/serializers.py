from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    '''
        This serializer is used for registering the
        user and validating the passwords.
    '''
    confirm_password = serializers.CharField(max_length = 16)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']
    
    def validate(self, attrs):
        '''
            Checks 2 conditions: 
            1. Passed password values must be equal.
            2. An User instance with the passed username must not exist.
        '''
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValueError('Make sure to pass the same password to confirm it!')
        if User.objects.filter(username = attrs.get('username')).exists():
            raise ValueError('Account with the given username already exists.')
        return attrs
    