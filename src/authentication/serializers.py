from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    '''
        This endpoint is used for registering a new user.
        To do so, pass an username and 2 password fields:
        password and confirm_password. 
    '''
    confirm_password = serializers.CharField(max_length = 16, read_only = True)
    
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
    
class LoginSerializer(serializers.Serializer):
    '''
        This endpoint is used to log an user in.
        Pass a valid username and password pair as request params.
    ''' 
    username = serializers.CharField(max_length = 100)
    password = serializers.CharField(max_length = 50)

    def validate(self, attrs):
        '''
            We check if an account with the passed credentials
            exists in the User model.
        '''
        if authenticate(username = attrs.get('username'), password = attrs.get('password')):
            return True
        raise User.DoesNotExist('Make sure that the user with the given credentials exists!')
    
    def get_user(self):
        '''
            In order to get the tokens, we need the
            user instance.
        '''
        username = self.validated_data.get('username')
        return User.objects.get(username = username)