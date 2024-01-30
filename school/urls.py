from django.urls import path

from school.views import SchoolCreateApiView

urlpatterns = [
    path('create/', SchoolCreateApiView.as_view(), name='school-create'),
]
