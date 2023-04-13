from rest_framework import serializers

# models
from .models import User, Interest

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'full_name',
            'ocupation',
            'email',
            'is_active'
        )


class InterestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = ('__all__')

class InterestsSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = ('id','name')

class UserUpdateSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'full_name',
            'interests'
        )

class UserDetailsSerializer(serializers.ModelSerializer):

    interests = InterestsSimpleSerializer(many = True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'full_name',
            'interests'
        )