from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from blogs.models import Blog, Comment
from blogs.serializers import BlogCreateUpdateSerializer, BlogSerializer, CommentSerializer, CommentReactionSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
    
class IsAuthorOfBlog(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.blog.author == request.user

class DraftBlogView(generics.CreateAPIView):
    serializer_class = BlogCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UpdateBlogView(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

class ListBlogView(generics.ListAPIView):
    queryset = Blog.objects.filter(status='published')
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'category', 'tags']
    search_fields = ['title', 'blog_content', 'author__username', 'category__name', 'tags__name']
    permission_classes = [IsAuthenticated]

class DeleteBlogView(generics.DestroyAPIView):
    queryset = Blog.objects.filter(status='published')
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

class DetailBlogView(generics.RetrieveAPIView):
    queryset = Blog.objects.filter(status='published')
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

class AddCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ReactionCommentView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentReactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        reaction = serializer.validated_data.get('reaction')
        instance = self.get_object()
        
        if reaction == 1:
            instance.upvotes += 1
            instance.save()
            
        elif reaction == 2:
            instance.downvotes += 1
            instance.save()

        return instance
    
class DeleteCommentView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOfBlog]