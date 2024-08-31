from rest_framework import serializers
from django.core.mail import send_mail
from blogs.models import Blog, Comment, Category, Tag
from blog_app.settings import DEFAULT_FROM_EMAIL

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'blog_content', 'category', 'tags', 'status']

    def __init__(self, *args, **kwargs):
        super(BlogCreateUpdateSerializer, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields['title'].required = False
            self.fields['blog_content'].required = False
            self.fields['tags'].required = False

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'blog', 'author', 'content', 'created_at', 'upvotes', 'downvotes']

    def create(self, validated_data):
        comment = super().create(validated_data)
        
        blog = comment.blog
        author_email = blog.author.email

        if comment.author != blog.author:
            subject = f"New Comment on Your Blog: {blog.title}"
            message = f"Hi {blog.author.username},\n\n" \
                    f"{comment.author.username} has commented on your blog post titled '{blog.title}'.\n\n" \
                    f"Comment: {comment.content}\n\n" \
                    f"Best regards,\nParth Jasani & Team"
            
            send_mail(
                subject,
                message,
                DEFAULT_FROM_EMAIL,
                [author_email],
                fail_silently=False,
            )

        return comment
    
class CommentReactionSerializer(serializers.ModelSerializer):
    reaction = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Comment
        fields = ['reaction']
    
    def validate(self, attr):
        if attr.get('reaction') not in [1, 2]:
            raise serializers.ValidationError("Invalid reaction")
        return attr


class BlogSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'publication_date', 'author', 'blog_content', 'category', 'tags', 'status', 'comment_count', 'comments']

    def get_author(self, obj):
        return obj.author.username
    
    def get_category(self, obj):
        return obj.category.name if obj.category else None
    
    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]