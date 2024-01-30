from django.urls import path

from user import views
from user.views import TokenDecodeView

urlpatterns = [
    path('create/', views.UserCreateApiView.as_view(), name='create'),
    path('me/', views.UserRetrieveApiView.as_view(), name='me'),
    path('token/decode/', TokenDecodeView.as_view(), name='token_decode'),
]
