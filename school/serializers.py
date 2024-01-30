from rest_framework.serializers import ModelSerializer

from school.models import School


class SchoolModelSerializer(ModelSerializer):
    class Meta:
        model = School
        fields = ['name', 'number', 'address', 'description']
