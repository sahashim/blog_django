from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import CustomUser

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    age = serializers.IntegerField()
    education = serializers.CharField()
    bio = serializers.CharField()
    image = serializers.ImageField()

    class Meta:
        model = CustomUser
        fields = ('password', 'email', 'first_name', 'last_name', 'age', 'bio', 'education', 'image')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': False},
            'age':{'required': False},
            'education':{'required': False},
            'bio':{'required': False},
            'image':{'required': False},
        }

    def validate(self, data):
        if CustomUser.objects.filter(username = data['email']).exists():
            raise serializers.ValidationError('username is token')
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
                                              email=validated_data['email'],
                                              password=validated_data['password'],
                                              first_name=validated_data['first_name'],
                                              last_name=validated_data['last_name'],
                                              age=validated_data['age'],
                                              education=validated_data['education'],
                                              bio=validated_data['bio'],
                                              image=validated_data['image'],
                                              )
        user.set_password(validated_data['password'])
        return validated_data


class EditSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    age = serializers.IntegerField()
    education = serializers.CharField()
    bio = serializers.CharField()
    image = serializers.ImageField()
    password=serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('password', 'email', 'first_name', 'last_name', 'age', 'bio', 'education', 'image')
        extra_kwargs = {
            'first_name': {},
            'last_name': {},
            'age':{},
            'education':{},
            'bio':{},
            'image':{},
        }

    def validate(self, data):
        user = authenticate(email=data['email'],password=data['password'])
        if  user:
            print('we got the bomb')
            user.is_active=False
            return data
        raise serializers.ValidationError({"email": "there is no any user with this email"})



    def update(self, instance, validated_data):

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.bio = validated_data['bio']
        instance.education = validated_data['education']
        instance.age = validated_data['age']
        instance.image = validated_data['image']
        instance.save()

        return instance



class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance