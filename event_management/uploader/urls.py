from django.urls import path, re_path
from .views import show_view, upload_view, profile_view, get_status_loader, loader_view, search_view

urlpatterns = [
    path('', show_view, name="Show View"),
    re_path(r'upload/$', upload_view, name="Upload File"),
    re_path(r'profile/(?P<id>[0-9]+)/$', profile_view, name="Profile View"),
    re_path(r'loader/$', loader_view, name="Loader View"),
    re_path(r'loaderStatus/$', get_status_loader, name="Get Status Of Loader"),
    re_path(r'search/$', search_view, name="Search View"),
]
