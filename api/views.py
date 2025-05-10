import json
import os
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer, UserSerializer, FileUploadSerializer
from .models import FileUpload
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
def get_tokens_for_user(user):
   
    refresh = RefreshToken.for_user(user)
    
  
    refresh['username'] = user.username
    refresh['role'] = user.role
    refresh['user_id'] = user.id
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    
    def create(self, request, *args, **kwargs):
        print(f"Registration request data: {request.data}")

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = serializer.save()
            tokens = get_tokens_for_user(user)

            response = Response({
                "message": "User registered successfully",
                "username": user.username,
                "access": tokens['access'],
                "refresh": tokens['refresh']
            }, status=status.HTTP_201_CREATED)

           
            response.set_cookie("access_token", tokens['access'])

            return response

        except Exception as e:
            print(f"Exception in registration: {str(e)}")
            return Response({
                "error": "Registration failed",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserProfileView(APIView):
    permission_classes = []  # Remove all permission checks

    def get(self, request):
        jwt_payload = getattr(request, 'jwt_payload', {})

        print(f"JWT Payload in UserProfileView: {jwt_payload}")
        print(f"Request user: {jwt_payload.get('role')}")

       
        if hasattr(request, 'user') and hasattr(request.user, 'role'):
            return Response({
                'id': jwt_payload.get('user_id'),
                'username': request.user.username,
                'role': request.user.role
            })

        # Fallback if user object not properly set
        return Response({
            'id': jwt_payload.get('user_id'),
            'username': jwt_payload.get('username'),
            'role': jwt_payload.get('role', 'user')
        })




@csrf_exempt
@require_http_methods(["GET", "POST"])
def admin_messages(request):
    # Pas de vérification de rôle ici pour maintenir la vulnérabilité JWT
    
    # Chemin pour stocker les messages
    messages_file = os.path.join(settings.BASE_DIR, 'admin_messages.json')
    
    # Initialiser les messages par défaut
    default_messages = [
        {"author": "Admin", "content": "Welcome to the SecOps dashboard"},
        {"author": "System", "content": "Daily security scan completed. No critical issues found."}
    ]
    
    # Récupération des messages existants
    if os.path.exists(messages_file):
        try:
            with open(messages_file, 'r') as f:
                stored_messages = json.load(f)
        except:
            stored_messages = default_messages
    else:
        stored_messages = default_messages
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            author = data.get('author', 'User')
            
            # Ajouter le nouveau message
            if not '<img' in message.lower() and not 'onerror' in message.lower() and not '<script' in message.lower():
                stored_messages.append({"author": author, "content": message})
            
            # Limiter le nombre de messages stockés
            if len(stored_messages) > 20:
                stored_messages = stored_messages[-20:]
            
            # Sauvegarder les messages
            with open(messages_file, 'w') as f:
                json.dump(stored_messages, f)
            
            # MODIFIED: Simplified XSS detection to make basic image payload work
            # Flag for any XSS attempt including the simple img onerror payload
            if '<img' in message.lower() and 'onerror' in message.lower():
                return JsonResponse({
                    "messages": stored_messages,
                    "secretFlag": "CTF{XSS_JWT_M4ST3R_H4CK3R}"
                })
            
            return JsonResponse({"messages": stored_messages})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    else:  # GET request
        # Révéler le flag si demandé explicitement
        flag_request = request.GET.get('getflag', '').lower() == 'true'
        
        if flag_request:
            return JsonResponse({
                "messages": stored_messages,
                "secretFlag": "CTF{XSS_JWT_M4ST3R_H4CK3R}"
            })
        
        return JsonResponse({"messages": stored_messages})
# Template views
def index_view(request):
    return render(request, 'index.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def admin_panel_view(request):
    return render(request, 'admin_panel.html')