from django.urls import path
from . import views

urlpatterns = [
    path("follow/", views.follow_create, name="follow"),
    path("like/", views.like_create, name="like"),
    path("comment/", views.commentview, name="comment"),
    path("comment/<int:pk>/", views.update_comment_view),
    path("comments/<int:pk>/", views.comment_delete_view),
]
