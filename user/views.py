from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from user.permissions import UserPermission
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


class UserRetrieveApiView(ListAPIView):
    permission_classes = [UserPermission]
    serializer_class = UserModelSerializer

    def get_queryset(self):
        user = self.response.user
        if user.is_authenticated:
            return AdminUser.objects.all()
        else:
            AdminUser.objects.none()

    def user_list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


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
