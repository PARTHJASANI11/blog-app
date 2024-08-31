from django.urls import path
from blogs.views import DraftBlogView, UpdateBlogView, ListBlogView, DeleteBlogView, DetailBlogView, AddCommentView, ReactionCommentView, DeleteCommentView

urlpatterns = [ 
    path('draft', DraftBlogView.as_view(), name="create_draft_blog"),
    path('<int:pk>/edit', UpdateBlogView.as_view(), name="edit_blog"),
    path('<int:pk>/detail', DetailBlogView.as_view(), name="detail_blog"),
    path('', ListBlogView.as_view(), name="list_blog"),
    path('<int:pk>/delete', DeleteBlogView.as_view(), name="delete_blog"),
    path('comments', AddCommentView.as_view(), name="add_comment"),
    path('<int:pk>/comments', ReactionCommentView.as_view(), name="add_reaction_comment"),
    path('<int:pk>/comments/delete', DeleteCommentView.as_view(), name="delete_comment"),
]