from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet,
                       get_confirmation_code, get_jwt_token)

router = DefaultRouter()
router.register('genres', GenreViewSet, basename='Genre')
router.register('categories', CategoryViewSet, basename='Category')
router.register('titles', TitleViewSet, basename='Title')
router.register('users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='Reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='Comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/email/', get_confirmation_code),
    path('v1/auth/token/', get_jwt_token),
    path('v1/users/me/', UserViewSet.as_view({'patch': 'partial_update'})),
]
