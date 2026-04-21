from django.urls import path
from blog.views import (ListView,
                        PostDetailView,
                        CommentUpdateView,
                        CommentDeleteView)

urlpatterns = [
    path("", ListView.as_view(), name="index"),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/update",
         CommentUpdateView.as_view(),
         name="comment-update"),
    path("posts/<int:pk>/delete",
         CommentDeleteView.as_view(),
         name="comment-delete"),
]
app_name = "blog"
