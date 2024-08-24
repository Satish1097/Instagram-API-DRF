from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from .models import Post, Profile, Follow, Comment, Story, like
from .serializers import (
    PostSerializer,
    ProfileSerialzer,
    StorySerializer,
    FollowSerializer,
    CommentSerializer,
    likeSerializer,
)
from django.db.models import Count
from django.contrib.auth.models import AnonymousUser


class PostViewSets(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        user = request.user
        x = list(
            Follow.objects.values_list("following", flat=True).filter(
                follower_id=user.id
            )
        )
        x.append(user.id)
        if isinstance(user, AnonymousUser):
            return Post.objects.none()
        return (
            queryset.filter(user_id__in=x)
            .annotate(comment_count=Count("comments"))
            .all()
            .order_by("-timestamp")
        )

    def destroy(self, request, **kwargs):
        instance = self.get_object()
        user = request.user

        # Check if the user is authenticated and is the owner of the post
        if user.is_authenticated and instance.user == user:
            self.perform_destroy(instance)
            return Response(
                {"success": "deleted Successfully"}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {"error": "You are not authorized to delete this post."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def update(self, request, **kwargs):
        instance = self.get_object()
        user = request.user
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        if user.is_authenticated and instance.user == user:
            self.perform_update(serializer)
            return Response({"success": "updated successfully"})
        else:
            return Response(
                {"error": "You are not authorized to update this Post."},
                status=status.HTTP_403_FORBIDDEN,
            )


class ProfileVieWSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerialzer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_authenticated:
            return queryset
        else:
            return Profile.objects.none()

    def create(self, request):
        user = request.user
        profile_exists = Profile.objects.filter(user=user).exists()

        if profile_exists:
            return Response(
                {"error": "Profile already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = self.get_serializer(data=self.request.data)
            if serializer.is_valid():
                serializer.save(
                    user=user
                )  # Assuming the serializer is a model serializer
                return Response(
                    {"success": "Profile created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, **kwargs):
        instance = self.get_object()
        user = self.request.user
        profile_picture = request.FILES.get("profile_picture")

        if profile_picture:
            instance.profile_picture = profile_picture

        if user.is_authenticated and instance.user == user:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # Let the serializer handle the profile update, including the profile picture
            return Response({"success": "updated successfully"})
        else:
            return Response(
                {"error": "You are not authorized to update this Profile."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def destroy(self, request, **kwargs):
        instance = self.get_object()
        user = request.user

        if user.is_authenticated and instance.user == user:
            self.perform_destroy(instance)
            return Response(
                {"success": "Deleted."},
            )
        else:
            return Response(
                {"error": "You are not authorized to delete this Profile."},
                status=status.HTTP_403_FORBIDDEN,
            )


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        user = request.user
        x = list(
            Follow.objects.values_list("following", flat=True).filter(
                follower_id=user.id
            )
        )
        x.append(user.id)
        if not user.is_authenticated:
            return Story.objects.none()
        return queryset.filter(user_id__in=x).all()

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user

        if user.is_authenticated and instance.user == user:
            self.perform_destroy(instance)
            return Response(
                {"success": "Deleted Successfully"},
            )
        else:
            return Response(
                {"error": "You are not authorized to delete this story."},
                status=status.HTTP_403_FORBIDDEN,
            )


# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     # lookup_field = "post_id"

#     # def retrieve(self, request, **kwargs):
#     #     post_id = self.kwargs.get("post_id")
#     # comments = Comment.objects.filter(post_id=post_id)
#     # serializer = self.get_serializer(comments, many=True)
#     # return Response(serializer.data)

#     def perform_create(self, serializer):
#         user = self.request.user
#         post_id = serializer.validated_data.get("post_id")
#         post = Post.objects.get(id=post_id)
#         text = serializer.validated_data.get("text")
#         serializer.save(post=post, text=text, user=user)

#     def update(self, request, *args, **kwargs):
#         print(kwargs)
#         instance = self.get_object()
#         user = request.user
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)

#         if user.is_authenticated and instance.user == user:
#             self.perform_update(serializer)
#             return Response({"success": "updated successfully"})
#         else:
#             return Response(
#                 {"error": "You are not authorized to update this comment."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#     def destroy(self, *args, **kwargs):
#         instance = self.get_object()
#         user = self.request.user

#         if user.is_authenticated and instance.user == user:
#             self.perform_destroy(instance)
#             return Response(
#                 {"success": "Deleted Successfully"},
#             )
#         else:
#             return Response(
#                 {"error": "You are not authorized to delete this comment."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )


# class FollowViewSet(viewsets.ModelViewSet):
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializer

#     def create(self, request, *args, **kwargs):
#         follower_id = self.request.query_params.get("follower_id")
#         user_id = request.user

#         user = request.user
#         print(follower_id)
#         print(user.id)

#         follower_id = kwargs.get("follower_id")
#         # Check if the follow relationship already exists
#         existing_follow = Follow.objects.filter(
#             following_id=follower_id, follower_id=user_id
#         ).first()

#         if existing_follow:
#             existing_follow.delete()
#             return Response({"success": "Unfollowed Successfully"})
#         else:
#             serializer = self.get_serializer()
#             serializer.save(follower_id=follower_id, user_id=user_id)
#             self.perform_create(self, serializer)

# def create(self, request):
#     following_user_id = request.data.get("following")
#     follower_user_id = request.data.get("follower")

# # Check if the follow relationship already exists
# existing_follow = Follow.objects.filter(
#     following_id=following_user_id, follower_id=follower_user_id
# ).first()

#     if existing_follow:
#         existing_follow.delete()  # If the relationship exists, delete it to "unfollow"
#         return Response("Unfollowed successfully", status=status.HTTP_200_OK)
#     elif following_user_id == follower_user_id:
#         return Response({"error": "You can't follow yourself"})
#     else:
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LikeViewSet(viewsets.ModelViewSet):
#     queryset = like.objects.all()
#     serializer_class = likeSerializer

#     def create(self, request, *args, **kwargs):
#         post_id = request.data.get("post")
#         user_id = request.data.get("user")

#         # Check if the follow relationship already exists
#         existing_like = like.objects.filter(post_id=post_id, user_id=user_id).first()

#         if existing_like:
#             existing_like.delete()  # If the relationship exists, delete it to "unfollow"
#             return Response("like removed successfully", status=status.HTTP_200_OK)
#         else:
#             serializer = self.get_serializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
