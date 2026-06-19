"""
URL configuration for dangerousapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.http import HttpResponseNotFound
from django.templatetags.static import static
from django.urls import include, path
from django.views.generic import RedirectView

def root_hidden(req):
    return HttpResponseNotFound()

urlpatterns = [
    path("", root_hidden),
    path("admin-access/", admin.site.urls),
    path("v1/", include("shows.urls")),
    path("favicon.ico", RedirectView.as_view(url=static("admin/img/favicon.png"), permanent=True))
]
