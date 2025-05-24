from rest_framework import serializers
from account.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, Token
from tokenize import TokenError
from datetime import datetime, timedelta
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name','gender','blood_group', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password doesn't match.")
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class SendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=6)

class VerifyEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=8)
    
class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    is_staff = serializers.BooleanField(read_only=True)
    class Meta:
        model=User
        fields = ['username','email', 'first_name', 'last_name', 'blood_group', 'image', 'phone', 'gender', 'address', 'last_donation_date', 'total_donated', 'is_available', 'is_staff']

class UserLoginSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(many=False, read_only=True)
    email = serializers.EmailField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'user_details', 'access_token', 'refresh_token']

    

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, please try again")
        if not user.is_active:
            raise AuthenticationFailed("Email is not verified")

        user_tokens = user.tokens()
        return {
            'user_details': user,
            'access_token': user_tokens.get('access'),
            'refresh_token': user_tokens.get('refresh')
        }
    
class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    default_error_messages = {
    'bad_token': ("Token is Invalid or has expired.")
  }
    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs
  
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail("bad_token")
        return