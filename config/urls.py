
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v2/users/",include("users.urls")),
    path("api/v2/pets/", include("pets.urls")),
    path("api/v2/posts/", include("posts.urls")),
    path("api/v2/categories/", include("categories.urls")),
    path("api/v2/auths/", include("auths.urls")),
    path("api/v2/bookmarks/", include("bookmarks.urls")),
    path("api/v2/likes/", include("likes.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
