from rest_framework import generics, permissions
from rest_framework_simplejwt import authentication

from school.serializers import SchoolModelSerializer


class SchoolCreateApiView(generics.CreateAPIView):
    serializer_class = SchoolModelSerializer
    # authentication_classes = [authentication.JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
