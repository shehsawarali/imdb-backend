from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tsv/", include("tsv.urls")),
    path("user/", include("users.urls")),
    path("", include("core.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

admin.site.site_header = "Filmfilia"
admin.site.site_url = ""
admin.site.unregister(Group)
