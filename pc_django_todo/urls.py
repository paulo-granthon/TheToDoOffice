"""pc_django_todo URL Configuration

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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    path('', include('authentication.urls')),
    path('', include('folders.urls'))
]

htmx_urlpatterns = [

    path('close_modal', views.close_modal, name="close_modal"),
    path('theme', views.switch_theme, name="theme"),

]

urlpatterns += htmx_urlpatterns


if settings.DEBUG:
    s = settings.STATIC_URL
    m = settings.MEDIA_URL
    print('urls.py DEBUG is True, adding STATIC_URL: "' + s + '" and "' + m + '" to urls')
    print('============================================')
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    print('urls.py DEBUG is False')
    print('============================================')
