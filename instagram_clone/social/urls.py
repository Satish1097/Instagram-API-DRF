from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r"posts", views.PostViewSets),
router.register(r"profile", views.ProfileVieWSet),
router.register(r"story", views.StoryViewSet),
# router.register(r"comment", views.CommentViewSet),
# router.register(r"follow", views.FollowViewSet),
# router.register(r"like", views.LikeViewSet),


urlpatterns = [
    path("auth/", obtain_auth_token),
    path("", include(router.urls)),
    # path('^follow/(?P<follower_id>.+)/$', views.FollowViewSet.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
