from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, SignUpViewSet, TitleViewSet,
                       TokenViewSet, UserViewSet)

r"^posts/(?P<post_id>\d+)/comments"
router = DefaultRouter()
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"titles", TitleViewSet, basename="titles")
router.register(r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews")
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>[\d]+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register(r"users", UserViewSet, basename="users")
router.register("auth/signup", SignUpViewSet, basename="sign-up")
router.register("auth/token", TokenViewSet, basename="token")


urlpatterns = [
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
    path("v1/", include(router.urls)),
    # path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    # path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
