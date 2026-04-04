# from rest_framework import status, generics, permissions
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from .serilaizers import RegistrationSerializer, LoginSerializer
#
# class RegisterView(generics.GenericAPIView):
#     serializer_class = RegistrationSerializer
#     permission_classes = [permissions.AllowAny]
#
#
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#
#         # Create JWT token pair
#         refresh = RefreshToken.for_user(user)
#
#         return Response({
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#             "user": serializer.data
#         }, status=status.HTTP_201_CREATED)
#
#
# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         user = serializer.validated_data['user']
#
#         refresh = RefreshToken.for_user(user)
#
#         return Response({
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#             "email": user.email,
#             "user_id": user.id,
#             "first_name": user.first_name,
#             "client_status": user.client_status,
#         }, status=status.HTTP_200_OK)