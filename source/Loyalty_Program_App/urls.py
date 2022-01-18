from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("clientapi.urls")),
]

urlpatterns += i18n_patterns(
    path('', include('merchantapp.urls')),
    path('accounts/', include("accounts.urls")),
    path('web/', include('webapp.urls'))
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
