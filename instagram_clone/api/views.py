from django.shortcuts import render
from rest_framework import mixins, generics
from rest_framework import status
from rest_framework.response import Response
from social.models import Profile, Follow, like, Comment
from django.contrib.auth.models import User
from social.serializers import (
    ProfileSerialzer,
    FollowSerializer,
    likeSerializer,
    CommentSerializer,
)


class FollowCreateAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get(self, request):
        user = request.user
        followings = Follow.objects.filter(follower_id=user.id)
        serializer = self.get_serializer(followings, many=True)
        return Response(serializer.data)

    def post(self, request):
        following_id = self.request.query_params.get("following_id")
        user = request.user
        user_id = user.id
        print(f"following id: {following_id}")
        print(f"user id: {user.id}")
        # Check if the follow relationship already exists
        existing_follow = Follow.objects.filter(
            follower_id=user_id, following_id=following_id
        ).first()
        if existing_follow:
            existing_follow.delete()
            return Response({"success": "Unfollowed Successfully"})
        else:
            Follow.objects.create(following_id=following_id, follower_id=user_id)
            return Response({"success": "Followed Successfully"})


follow_create = FollowCreateAPIView.as_view()


class likeCreateAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = like.objects.all()
    serializer_class = likeSerializer

    def get(self, *args, **kwargs):
        post_id = self.request.query_params.get("post_id")
        likes = like.objects.filter(post_id=post_id)
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        post_id = self.request.query_params.get("post_id")

        user = request.user
        user_id = user.id
        print(f"post id: {post_id}")
        print(f"user id: {user_id}")
        # Check if the like already exists
        existing_like = like.objects.filter(post_id=post_id, user_id=user_id).first()

        if existing_like:
            existing_like.delete()
            return Response({"success": "like removed Successfully"})
        else:
            like.objects.create(user_id=user_id, post_id=post_id)
            return Response({"success": "like added Successfully"})


like_create = likeCreateAPIView.as_view()


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"

    def get(self, *args, **kwargs):
        post_id = self.request.query_params.get("post_id")
        print(f"post_id:{post_id}")
        comments = Comment.objects.filter(post_id=post_id)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):  # http -> post
        post_id = self.request.query_params.get("post_id")
        text = self.request.data.get("text")
        user_id = request.user.id

        print(f"post_id:{post_id}")
        print(f"user_id:{user_id}")

        if request.user.is_authenticated:
            Comment.objects.create(post_id=post_id, user_id=user_id, text=text)
            return Response({"success": "comment created successfully"})


commentview = CommentViewSet.as_view()


class CommentUpdateAPIView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"

    def update(self, request, **kwargs):
        user = request.user
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            if user.is_authenticated and instance.user == user:
                serializer.save()
                return Response({"message": "updated successfully"})
            else:
                return Response(
                    {"message": "you are not authorized to update this comment"}
                )


update_comment_view = CommentUpdateAPIView.as_view()


class CommentDeleteAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if user.is_authenticated and instance.user == user:
            self.perform_destroy(instance)
            return Response({"success": "deleted Successfully"})
        else:
            return Response({"error": "you are not authorized to delete this comment"})


comment_delete_view = CommentDeleteAPIView.as_view()
