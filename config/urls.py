
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/users/",include("users.urls")),
    path("api/v1/pets/", include("pets.urls")),
    path("api/v1/posts/", include("posts.urls")),
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/auths/", include("auths.urls")),
    # path("api/v1/bookmarks", include("bookmarks.urls")),
    path("api/v1/likes", include("likes.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
