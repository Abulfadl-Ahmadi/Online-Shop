from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Address


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password_confirm', 'phone_number', 'date_of_birth']
        extra_kwargs = {
            'password': {"write_only": True},
            'phone_number': {"read_only": True},
            'date_of_birth': {"read_only": True}
        }

    def validate(self, data):
        if 'password' not in data or 'password_confirm' not in data:
            raise serializers.ValidationError('Password and password confirmation are required.')
        
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Passwords do not match.')
        
        return data
    


    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password', None)
        userInstance = self.Meta.model(**validated_data)
        userInstance.set_password(password)
        userInstance.save()
        return userInstance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # Add more fields as needed
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def update(self, instance, validated_data):
        # Update user fields with validated data
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance




class AddressSerializer(serializers.ModelSerializer):
    class meta:
        fields = [
            'id',
            'country',
            'state',
            'city',
            'street_address',
            'postal_code',
            'is_primary',
        ]