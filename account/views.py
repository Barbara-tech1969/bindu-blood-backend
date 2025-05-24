from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets, permissions
from account.models import User, OneTimePassword
from rest_framework.response import Response
from account.utils import generate_otp, send_template_email, delete_instance_after
from rest_framework.exceptions import MethodNotAllowed
from account.serializers import UserRegistrationSerializer, UserSerializer,SendOtpSerializer,UserLoginSerializer, LogoutUserSerializer, VerifyEmailSerializer
from account.paginations import UserProfilePagination
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)
        otp = generate_otp(user)
        send_template_email(
            subject="Activate your email on Bindu",
            templateName="confirm_email.html",
            toEmail=user.email,
            context={"fullName": user.username, "otp": otp}
        )
        return Response(
            {
                "user": serializer.data,
                "message": "Account creation successful. Please check your email to verify."
            },
            status=status.HTTP_201_CREATED
        )

class SendOtpView(generics.GenericAPIView):
    serializer_class = SendOtpSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        if user:
            otp = generate_otp(user)
            send_template_email(
                subject="Active your email on Bindu",
                templateName="confirm_email.html", 
                toEmail=user.email, 
                context={"fullName":user.username,
                    "otp": otp}
                    )
            return Response(
                {
                    "New OTP has been sent to your email. check again."
                }, status=status.HTTP_200_OK
            )
        # if there is no user with the email
        return Response(
            {
                "error": "Invalid Email, Please enter correct email."
            }, status=status.HTTP_404_NOT_FOUND
        )

class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data.get('otp')
        try:
            user_otp_instance = OneTimePassword.objects.get(otp=otp)
            valid_otp = delete_instance_after(user_otp_instance, 5)  # Checking OTP expiry period for five minutes
            if valid_otp:
                user = user_otp_instance.user
                user.is_active = True
                user.save()
                return Response(
                    {'message': 'Account email verified successfully.'},
                    status=status.HTTP_202_ACCEPTED
                )
            else:
                return Response(
                    {'error': 'OTP expired. Try again.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except OneTimePassword.DoesNotExist:
            return Response(
                {'error': 'OTP not provided.'},
                status=status.HTTP_404_NOT_FOUND
            )

        
class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.AllowAny,]
    parser_classes = (MultiPartParser, FormParser,)
    pagination_class = UserProfilePagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get','delete','patch')
    lookup_field = 'username'
    filterset_fields = ['is_available', 'blood_group']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username', 'email']
    
class LoginUserView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LogoutUserView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LogoutUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
