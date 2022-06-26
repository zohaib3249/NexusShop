
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import  i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
urlpatterns =[
    path('i18n/', include('django.conf.urls.i18n'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




urlpatterns += i18n_patterns(
    path(r'admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls', namespace='core')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)