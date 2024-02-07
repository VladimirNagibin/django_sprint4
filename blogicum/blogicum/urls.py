from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from blog.views import UserCreateView

urlpatterns = [
    path('admin/',
         admin.site.urls),
    path('auth/registration/',
         UserCreateView.as_view(),
         name='registration'),
    path('auth/',
         include('django.contrib.auth.urls')),
    path('',
         include('blog.urls', namespace='blog')),
    path('pages/',
         include('pages.urls', namespace='pages')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
