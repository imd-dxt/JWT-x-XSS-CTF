# urls.py
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import (
    CustomTokenObtainPairView,
    RegisterView, 
    UserProfileView, 
    admin_messages,
    index_view,
    dashboard_view,
    admin_panel_view
)

urlpatterns = [
    # API endpoints
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    
    
    # Template views
    path('', index_view, name='index'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('admin-panel/', admin_panel_view, name='admin_panel'),
    path('api/admin/messages/', admin_messages, name='admin_messages'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)