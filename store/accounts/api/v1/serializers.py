from django.db.models import fields
from django.forms import ValidationError
from rest_framework import serializers
from ...models import Profile, User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    phone_number = serializers.CharField(
            required=True,
            max_length=9,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone_number', 'password', 'password2')
        extra_kwargs = {
            'full_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # fields = '__all__'
        exclude = ['user', ]




class LoginPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=9)



class LoginPhoneNumberSerializerValidCode(serializers.Serializer):
    phone_number = serializers.CharField(max_length=9)
    code = serializers.CharField(max_length=5)

