from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import FileUpload, User
from django.conf import settings
import mimetypes
import os
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Ajoute les claims personnalisés
        token['username'] = user.username
        token['role'] = user.role
        return token


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
        extra_kwargs = {
            'username': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Custom validation can be added here
        return attrs

    def create(self, validated_data):
        # Remove the password2 field as it's not needed for user creation
        validated_data.pop('password2', None)
        
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password']
            )
            user.role = 'user'  # Set default role
            user.save()
            return user
        except Exception as e:
            # Log the error in your production environment
            print(f"Error creating user: {str(e)}")
            raise serializers.ValidationError({"detail": "Error creating user"})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'role')
        read_only_fields = ('id', 'role')

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ('file', 'content_type')
        read_only_fields = ('content_type',)
    
    def validate_file(self, value):
        # Check file size
        if value.size > settings.MAX_UPLOAD_SIZE:
            raise serializers.ValidationError(f"File size cannot exceed {settings.MAX_UPLOAD_SIZE/1024/1024}MB")
        
        # VULNERABLE: Only checking file extension, not actual content
        # This can be bypassed by renaming a malicious file to have an allowed extension
        file_ext = os.path.splitext(value.name)[1].lower()
        
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.txt', '.pdf', '.json'] 
        
        if file_ext not in allowed_extensions:
            raise serializers.ValidationError(f"Unsupported file type. Allowed extensions: {', '.join(allowed_extensions)}")
        
        # Map extensions to MIME types
        extension_to_mime = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.txt': 'text/plain',
            '.pdf': 'application/pdf',
            '.json': 'application/json'  # Added JSON
        }
        
        # Set the content type based on extension (VULNERABLE)
        value._content_type = extension_to_mime.get(file_ext, 'application/octet-stream')
        
        return value
    
    def create(self, validated_data):
        # Make sure we have a user in the request context
        user = self.context['request'].user
        validated_data['user'] = user
        
        # VULNERABLE: Using the potentially manipulated content type
        file_ext = os.path.splitext(validated_data['file'].name)[1].lower()
        extension_to_mime = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.txt': 'text/plain',
            '.pdf': 'application/pdf',
            '.json': 'application/json'  # Added JSON
        }
        validated_data['content_type'] = extension_to_mime.get(file_ext, 'application/octet-stream')
        
        return super().create(validated_data)