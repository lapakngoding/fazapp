from django.urls import path
from .views.setting_views import PortalSettingUpdateView
from .views.banner_views import BannerListView, BannerCreateView, BannerUpdateView

app_name = 'portal'

urlpatterns = [
    path('settings/', PortalSettingUpdateView.as_view(), name='settings'),
    path('banners/', BannerListView.as_view(), name='banner_list'),
    path('banners/create/', BannerCreateView.as_view(), name='banner_create'),
    path('banners/<int:pk>/edit/', BannerUpdateView.as_view(), name='banner_edit'),
]
