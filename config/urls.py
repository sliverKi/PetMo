
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/users/",include("users.urls")),
    path("api/v1/pets/", include("pets.urls")),
    path("api/v1/posts/", include("posts.urls")),
    path("api/v1/categories/", include("categories.urls")),
    # path("api/v1/pets/", include("pets.urls")),
]
