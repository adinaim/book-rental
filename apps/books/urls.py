from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentCreateDeleteView, TagViewSet, LikedPostView



router = DefaultRouter()
router.register('post', PostViewSet, 'post')
router.register('comment', CommentCreateDeleteView, 'comment')
router.register('tags', TagViewSet, 'tags')
urlpatterns = [
    path('liked/', LikedPostView.as_view(), name='liked')
]
urlpatterns += router.urls