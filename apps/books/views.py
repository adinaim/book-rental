from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import mixins, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as rest_filter
from rest_framework.generics import ListAPIView
# from rest_framework.generics import (
#     ListAPIView, 
#     RetrieveAPIView, 
#     DestroyAPIView, 
#     UpdateAPIView, 
#     CreateAPIView
#     )

from .models import (
    Post, 
    Comment, 
    Tag,
    Rating,
    Like
    )

from .serializers import (
    LikeSerializer,
    PostListSerializer, 
    PostSerializer, 
    CommentSerializer,
    PostCreateSerializer,
    CommentSerializer,
    RatingSerializer,
    TagSerializer,
    LikedPostSerializer
    )

from .permissions import IsOwner

    # один в один все
# class PostListView(ListAPIView):
#     # queryset = Post.objects.filter(status='open')
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [
        filters.SearchFilter, 
        rest_filter.DjangoFilterBackend, 
        filters.OrderingFilter
        ]
    search_fields = ['title', 'user__username'] # user нельзя, неподное поле
    filterset_fields = ['tag']
    ordering_fields = ['created_at']
    # pagination_class

    def perform_create(self, serializer): # для чего эта функция, чтобы не рописыать юзера в запрроме
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'create':
            return PostCreateSerializer
        return super().get_serializer_class() # вызывает дефолтный сериалайзер, а какой тут дефолтен

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action == 'comment' and self.request.method == 'DELETE':
            self.permission_classes = [IsOwner]
        if self.action in ['create', 'comment', 'set_rating', 'like']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions() # зачем давать доступ ко всему, если других действий не предусмотрено, там в рууте лежит AllowAny

    @action(detail=True, methods=['POST', 'DELETE'])
    def comment(self, request, pk=None):
        post = self.get_object() # в generics
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, post=post)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )      

    @action(methods=['POST', 'PATCH'], detail=True, url_path='set-rating')
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['post'] = pk                                                      # переписать cur user def # TODO
        serializer = RatingSerializer(data=data, context={'request': request})
        rate = Rating.objects.filter(
            user=request.user,
            post=pk
        ).first()
        if serializer.is_valid(raise_exception=True):
            if rate and request.method == 'POST':
                return Response(
                    {'detail': 'Rating object exists. Use PATCH method'}
                )
            elif rate and request.method =='PATCH':
                serializer.update(rate, serializer.validated_data)
                return Response('Updated')
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data)
            return Response({'detail': 'Rating obejct does ot exist. Use POST method'})

    @action(detail=True, methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        post = self.get_object()
        serializer = LikeSerializer(data=request.data, context={
            'request': request, 
            'post': post
            })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('Liked!')
            if request.method == "DELETE":
                serializer.unlike()
                return Response('Unliked!')

    
class CommentCreateDeleteView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner]


class TagViewSet(mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class LikedPostView(ListAPIView):
    serializer_class = LikedPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Like.objects.filter(user=user)