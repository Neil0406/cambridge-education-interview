from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from django.views import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'__hiddenadmin/', admin.site.urls),
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path('main/', include('app_main.urls'), name='app_main'),   
]

    
'''
swagger
'''
schema_view = get_schema_view(
   openapi.Info(
      title="CAMBRIDGE_EDUCATION_INTERVIEW API",
      default_version='v1',
      description="CAMBRIDGE_EDUCATION_INTERVIEW API",
   ),
    public=True,
    permission_classes = (AllowAny,)
    # permission_classes = (IsAdminUser,) #is_staff才可使用
)

urlpatterns += [
    re_path(r'^__hiddenswagger(?P<format>\.json|\.yaml)$', login_required(schema_view.without_ui(cache_timeout=0)), name='schema-json'),
    re_path(r'^__hiddenswagger/$', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    re_path(r'^redoc/$', login_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
    re_path(r'^accounts/', include('rest_framework.urls', namespace='rest_framework'))
]