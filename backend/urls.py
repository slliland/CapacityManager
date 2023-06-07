"""djangoHeroku URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from .api.views import index_view, UserViewSet, GroupViewSet, MessageViewSet

from . import views


router = routers.DefaultRouter()
router.register('messages', MessageViewSet)
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)

urlpatterns = [

    path('api/forecast/<str:date>/<int:range_value>/<int:cluster>', views.forecast, name='forecast'),
    path('api/forecast2/<str:date>/<int:range_value>/<int:cluster>', views.forecast2, name='forecast2'),

    # http://localhost:8000/
    path('', index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    path('api/explorer/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),
    # path('/generate-data/', views.generate_data, name='generate-data'),
    # path('api/csrf/', views.get_csrf, name='get_csrf'),
    # path('api/convert/', views.convert, name='convert'),
    # path('api/convert_to_uppercase/', convert_to_uppercase, name='convert_to_uppercase'),
]