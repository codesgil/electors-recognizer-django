from django.urls import include, path
from rest_framework import routers

from .views import upload_elector_picture_view, VoteView, CampaignView, ElectorView, get_elector_view, VoteOfficeView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'votes', VoteView)
router.register(r'campaigns', CampaignView)
router.register(r'electors', ElectorView)
router.register(r'votes-offices', VoteOfficeView)

urlpatterns = [
    path('api/v1/electors/upload', upload_elector_picture_view),
    path('api/v1/electors/matricule', get_elector_view),
    path('api/v1/', include(router.urls))
]
