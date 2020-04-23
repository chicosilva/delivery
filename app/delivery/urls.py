from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from gestao.urls import urls_gestao
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('gestao/', include((urls_gestao, 'gestao'), namespace='gestao'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
