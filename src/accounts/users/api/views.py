import logging

from rest_framework import generics, mixins, permissions
from rest_framework.response import Response

from .serializers import UserGETSerializer

logger = logging.getLogger(__name__)


class UserMeAPIView(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    serializer_class = UserGETSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
