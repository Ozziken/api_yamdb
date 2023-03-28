from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import GenreViewSet, TitleViewSet, CategoryViewSet

router = DefaultRouter()
router.register("genres", GenreViewSet, basename="genre")
router.register("categories", CategoryViewSet, basename="categories")
router.register("titles", TitleViewSet, basename="title")


urlpatterns = [
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
    path("v1/", include(router.urls)),
]
