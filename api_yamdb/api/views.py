from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from api.mixins import CreateUpdateDeleteViewSet
from api.permissions import (
    AuthorOrAdminOrModeratOrReadOnly,
    IsAdminOrReadOnly,
    IsAuthor,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleOnlyReadSerializer,
    TitleSerializer,
    TokenSerializer,
    UserMeSerializer,
    UserSerializer,
)

ALLOWED_METHODS = ("get", "post", "patch", "delete")


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(CreateUpdateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    search_fields = ["name"]
    filter_backends = [filters.SearchFilter]


class GenreViewSet(CreateUpdateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    search_fields = ["name"]
    filter_backends = [filters.SearchFilter]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    search_fields = ["name"]
    filter_backends = [filters.SearchFilter]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleOnlyReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет модели ревью на произведение."""

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorOrAdminOrModeratOrReadOnly,
    )
    pagination_class = PageNumberPagination
    serializer_class = ReviewSerializer

    def get_title(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Review, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет модели комментария к ревью на произведение."""

    permission_classes = (
        IsAuthor,
        AuthorOrAdminOrModeratOrReadOnly,
    )
    pagination_class = PageNumberPagination
    serializer_class = CommentSerializer

    def get_review(self):
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    filterset_fields = "username"
    search_fields = ("username",)
    permission_classes = (
        IsAuthenticated,
        IsAdminOrReadOnly,
    )
    http_method_names = ALLOWED_METHODS

    @action(
        methods=["get", "patch"],
        detail=False,
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def get(self, request):
        queryset = User.objects.get(username=request.user.username)
        serializer = UserMeSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if User.objects.filter(
            username=request.data.get("username"), email=request.data.get("email")
        ):
            user = User.objects.get(username=request.data.get("username"))
            serializer = SignUpSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = request.data.get("username")
            user = User.objects.get(username=username)
            code = user.confirmation_code
            send_mail(
                f"Добро пожаловать в YaMDb, {user.username}!",
                (f"Ваш confirmation_code: {code} "),
                "yamdb@yandex.ru",
                [request.data.get("email")],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenViewSet(viewsets.ViewSet):
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, username=request.data.get("username"))
            if str(user.confirmation_code) == request.data.get("confirmation_code"):
                refresh = RefreshToken.for_user(user)
                token = {"token": str(refresh.access_token)}
                return Response(token, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
