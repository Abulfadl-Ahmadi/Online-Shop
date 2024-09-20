
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()

class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]  # Ensure the user is authenticated

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        # Get the authenticated user
        user = request.user
        
        # Serialize the user data
        serializer = UserSerializer(user)
        
        # Return the serialized data
        return Response(serializer.data)

class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the authenticated user
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     def post(self, request):
#         username = request.data['username']
#         password = request.data['password']

#         user = User.objects.filter(username=username).first()
#         if user is None:
#             raise AuthenticationFailed('User not found!')
        
#         if not user.check_password(password):
#             raise AuthenticationFailed("Incorrect password!")
        

#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'ait': datetime.datetime.utcnow()
#         }
        
#         token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

#         responce = Response()
#         responce.set_cookie(key='jwt', value=token, httponly=True)
#         i = {'jwt': token}
#         responce.data = json.dumps(
#             i,
#             sort_keys=True,
#             indent=1,
#             cls=DjangoJSONEncoder
#             )

#         return responce
    

# class LoginView(APIView):
#     """
#     API view to handle user login and issue JWT tokens.
#     """
#     permission_classes = [AllowAny]
#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to handle user login with differentiated error messages for invalid username and password.
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if the username or password is missing
        if not username or not password:
            return Response(
                    {"detail": "Username and password are required."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Authenticate user using the custom backend
        try:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # If authentication is successful, continue with JWT token generation
                response = super().post(request, *args, **kwargs)
                
                access_token = response.data.get("access")
                refresh_token = response.data.get("refresh")

                # Set tokens in cookies
                response.set_cookie(
                    key="access_token",
                    value=access_token,
                    httponly=True,
                    secure=True,    # Use HTTPS in production
                    samesite='Lax', # For CSRF protection
                    max_age=60 * 5  # Access token expiry (e.g., 5 minutes)
                )
                
                response.set_cookie(
                    key="refresh_token",
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    max_age=60 * 60 * 24 * 7  # Refresh token expiry (e.g., 7 days)
                )

                return response
            else:
                # This should never be hit due to ValueError handling below
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        except ValueError as e:
            # Return a custom response depending on the specific ValueError raised
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        responce = Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        responce.delete_cookie('access_token')
        responce.delete_cookie('refresh_token')
        return responce
