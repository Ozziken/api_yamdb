from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                       UserViewSet, SignUpViewSet, TokenViewSet)

router = DefaultRouter()
router.register("genres", GenreViewSet, basename="genre")
router.register("categories", CategoryViewSet, basename="categories")
router.register("titles", TitleViewSet, basename="title")
router.register('users', UserViewSet, basename='users')
router.register('auth/signup', SignUpViewSet, basename='sign-up')
router.register('auth/token', TokenViewSet, basename='token')


urlpatterns = [
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
    path("v1/", include(router.urls)),
]
