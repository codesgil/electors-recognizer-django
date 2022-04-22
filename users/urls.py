from django.urls import include, path
from rest_framework import routers
from .views import UserView, logout_view, RefreshTokenView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, basename='UserView')

urlpatterns = [
    path('api/v1/logout', logout_view),
    path('api/v1/refresh-token', RefreshTokenView.as_view(), name='refresh_token'),
    path('api/v1/', include(router.urls))
]
