from django.urls import path
from .views.setting_views import PortalSettingUpdateView
from .views.banner_views import BannerListView, BannerCreateView, BannerUpdateView
from .views.post_views import PostListView, PostCreateView, PostUpdateView
from .views.public_views import LandingPageView, PostDetailView

app_name = 'portal'

urlpatterns = [
    path('settings/', PortalSettingUpdateView.as_view(), name='settings'),
    path('banners/', BannerListView.as_view(), name='banner_list'),
    path('banners/create/', BannerCreateView.as_view(), name='banner_create'),
    path('banners/<int:pk>/edit/', BannerUpdateView.as_view(), name='banner_edit'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('news/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
