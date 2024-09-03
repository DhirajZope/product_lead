from django.contrib import admin
from django.urls import path, include

# Third party imports
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
      title="Product Lead",
      default_version='v1',
      description="API documentation for Product Lead Assignment",
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('products/', include('products.urls')),
    path('leads/', include('leads.urls')),
    path('auth/', include('authentication.urls')),
]
