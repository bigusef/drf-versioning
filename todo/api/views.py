from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from todo.api.serializers import TaskSerializer
from todo.models import Task


class TaskViewSet(ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        print(self.request.version)

        if self.action == "list":
            return Task.objects.filter(parent__isnull=True)
        return Task.objects.all()
