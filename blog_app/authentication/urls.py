from django.urls import path
from authentication.views import RegisterView, CustomObtainTokenPairView, UserProfileUpdateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [ 
    path('register', RegisterView.as_view(), name="auth_register"),
    path('token', CustomObtainTokenPairView.as_view(), name="auth_token"),
    path('refresh-token', TokenRefreshView.as_view(), name="auth_refresh_token"),
    path('profile', UserProfileUpdateView.as_view(), name="update_profile")
]