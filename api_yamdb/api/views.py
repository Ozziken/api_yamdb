from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from .utils import check_confirmation_code

from api.mixins import CreateUpdateDeleteViewSet
from api.permissions import (
    AuthorOrAdminOrModeratOrReadOnly,
    IsAdminOrReadOnly,
    IsAuthor,
    IsAuthenticatedOrCreateOnly,
    IsAdminRole,
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


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(CreateUpdateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["name"]
    filter_backends = [filters.SearchFilter]
    lookup_field = "slug"
    search_fields = ("name",)
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=["delete"],
        url_path=r"(?P<slug>\w+)",
        lookup_field="slug",
        url_name="category_slug",
    )
    def get_category(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(CreateUpdateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["name"]
    filter_backends = [filters.SearchFilter]
    lookup_field = "slug"
    search_fields = ("name",)
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=["delete"],
        url_path=r"(?P<slug>\w+)",
        lookup_field="slug",
        url_name="category_slug",
    )
    def get_genre(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitleFilter
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve", "delete"):
            return TitleOnlyReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет модели ревью на произведение."""

    pagination_class = PageNumberPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorOrAdminOrModeratOrReadOnly,
    )
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет модели комментария к ревью на произведение."""

    permission_classes = (
        IsAuthenticatedOrCreateOnly,
        AuthorOrAdminOrModeratOrReadOnly,
    )
    pagination_class = PageNumberPagination
    serializer_class = CommentSerializer

    def get_review(self):
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["username", ]
    lookup_field = "username"
    permission_classes = [IsAuthenticated, IsAdminRole, ]
    pagination_class = PageNumberPagination

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = UserMeSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return UserSerializer
    #Response(serializer.data)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        if (User.objects.filter(username=request.data.get("username"),
                                email=request.data.get("email"))):
            user = User.objects.get(username=request.data.get("username"))
            serializer = SignUpSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = request.data.get('username')
            user = User.objects.get(username=username)
            code = user.confirmation_code
            send_mail(
                f'Добро пожаловать в YaMDb, {user.username}!',
                (f'Ваш confirmation_code: {code} '),
                'yamdb@yandex.ru',
                [request.data.get('email')],
                fail_silently=False,
            )
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class Token(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if check_confirmation_code(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': ['Код не действителен!']},
            status=status.HTTP_400_BAD_REQUEST
        )
