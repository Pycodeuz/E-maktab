from django.utils.translation import gettext as _
from rest_framework import serializers

from user.models import AdminUser

"""
Serializers for user API View.
"""

from django.contrib.auth import authenticate


class UserModelSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = AdminUser
        fields = ['phone', 'password', 'full_name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """create and return a user with encrypted password"""
        return AdminUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update and return a user with encrypted password"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class TokenDecodeSerializer(serializers.Serializer):
    token = serializers.CharField()
