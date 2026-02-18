"""
URL configuration for config project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.portal.views.public_views import LandingPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='index'),
    path('auth/', include('apps.core.urls', namespace='core')),
    path("users/", include("users.urls", namespace="users")),
    #path("core/", include("apps.core.urls")),
    #path("users/", include("apps.users.urls")),
    path('portal/', include('apps.portal.urls', namespace='portal')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

#handler403 = "apps.core.views.dashboard.permission_denied_view"
#handler404 = "apps.core.views.dashboard.page_not_found_view"

handler403 = "apps.core.views.errors.permission_denied_view"
handler404 = "apps.core.views.errors.page_not_found_view"

