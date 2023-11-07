from logging import getLogger

from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from todo.api.serializers import TaskSerializer
from todo.models import Task

logger = getLogger(__name__)


class TaskViewSet(ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        if self.request.version == "1.2.3":
            logger.info("You have using a version off `1.2.3`")

        if self.request.version >= "2.0.0":
            logger.info("have a new version in your api, take a decision you need")

        if self.action == "list":
            return Task.objects.filter(parent__isnull=True)
        return Task.objects.all()
