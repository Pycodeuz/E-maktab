from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from user.serializers import (
    UserModelSerializer
)
from .models import AdminUser
from .serializers import TokenDecodeSerializer

"""
Views for User Api.
"""


class UserCreateApiView(generics.CreateAPIView):
    """Creat new AdminUser  in the system"""
    serializer_class = UserModelSerializer


class UserRetrieveUpdateApiView(generics.RetrieveUpdateAPIView):
    serializer_class = UserModelSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


"""Custom Api for decode token"""


class TokenDecodeView(APIView):

    @swagger_auto_schema(request_body=TokenDecodeSerializer)
    def post(self, request):
        serializer = TokenDecodeSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            try:
                decoded_token = AccessToken(token)
                user_id = decoded_token['user_id']
                token_type = 'access'
            except TokenError:
                try:
                    decoded_token = RefreshToken(token)
                    user_id = decoded_token['user_id']
                    token_type = 'refresh'
                except TokenError as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            admin_user = AdminUser.objects.get(id=user_id)

            user_info = {
                'user_id': user_id,
                'token_type': token_type,
                'full_name': admin_user.full_name,
                'phone': admin_user.phone,
            }

            return Response(user_info, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
