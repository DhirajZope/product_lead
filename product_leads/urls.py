from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('leads/', include('leads.urls')),
    path('auth/', include('authentication.urls')),
]
