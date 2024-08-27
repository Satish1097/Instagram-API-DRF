from rest_framework import serializers
from .models import Post, Profile, like, Comment, Story, Follow
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username"]


class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "owner", "image", "caption", "timestamp", "likes"]

    def validate_like(self):
        like = self.likes
        if like > 0:
            raise serializers.ValidationError()
        return like


class ProfileSerialzer(serializers.ModelSerializer):
    owner = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "owner",
            "profile_picture",
            "bio",
            "created_on",
            "updated_on",
            "favorite",
        ]


class StorySerializer(serializers.ModelSerializer):
    owner = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Story
        fields = ["id", "owner", "file", "created_on"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "user", "text", "created_date"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "following", "follower"]


class likeSerializer(serializers.ModelSerializer):
    class Meta:
        model = like
        fields = ["id", "user", "post"]
