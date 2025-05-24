from django.urls import path,include
from account.views import UserRegistrationView, VerifyEmailView, UserProfileViewSet,SendOtpView,LoginUserView, LogoutUserView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register('',UserProfileViewSet,basename="profile-api")
urlpatterns = [
    path('profile/', include(router.urls)),
    path('register/',UserRegistrationView.as_view(), name='register-api'),
    path('verify-email/', VerifyEmailView.as_view(), name="verify-email-api"),
    path('otp/request/',SendOtpView.as_view(), name="send-otp-api"),
    path('login/',LoginUserView.as_view(), name="login-api"),
    path('logout/',LogoutUserView.as_view(), name="logout-api"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token-refresh-api"),
]
