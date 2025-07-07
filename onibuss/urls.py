from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # painel admin padrão do Django
    path('', include('principal.urls')),  # inclui as URLs do seu app principal
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
]