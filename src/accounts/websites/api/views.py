import logging

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import WebsiteGETSerializer
from ..models import Website

logger = logging.getLogger(__name__)


class WebsiteGETViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = WebsiteGETSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Website.objects.filter(user=self.request.user)
