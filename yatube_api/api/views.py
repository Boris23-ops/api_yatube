from rest_framework import permissions, viewsets
from rest_framework.generics import get_object_or_404

from api.serializer import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post
from .permissions import IsAuthor


class PostViewSet(viewsets.ModelViewSet):
    """Обрабатывает API запросы для модели Постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Обрабатывает API запросы для модели Групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Обрабатывает API запросы для модели Коментариев."""

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
