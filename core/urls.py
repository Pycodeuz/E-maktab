from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from core.drf_yasg import swagger_urls
from core.settings import STATIC_URL, STATIC_ROOT, MEDIA_ROOT, MEDIA_URL

urlpatterns = []
urlpatterns += swagger_urls + [
    path("admin/", admin.site.urls),
    path('account/', include('user.urls')),
    path('school/', include('school.urls')),
    path('token/create/', TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

] + static(STATIC_URL, document_root=STATIC_ROOT) + static(MEDIA_URL, document_root=MEDIA_ROOT)
