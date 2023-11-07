from logging import getLogger

from django.db import transaction
from rest_framework import serializers

from todo.models import Task

logger = getLogger(__name__)


class SubTaskSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Task.objects.filter(parent__isnull=False), required=False)
    title = serializers.CharField(max_length=75)
    description = serializers.CharField()
    created_at = serializers.ReadOnlyField()
    last_modified = serializers.ReadOnlyField()


class TaskSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=75)
    description = serializers.CharField()
    sub_tasks = SubTaskSerializer(many=True, allow_null=True, required=False)
    created_at = serializers.ReadOnlyField()
    last_modified = serializers.ReadOnlyField()

    @staticmethod
    def handle_sub_tasks(parent_task, validated_data: list[dict]):
        if not validated_data:
            return

        updated_tasks, created_tasks = [], []
        for task in validated_data:
            if id in task:
                updated_tasks.append(task)
            else:
                created_tasks.append(task)

        if created_tasks:
            Task.objects.bulk_create([Task(parent=parent_task, **data) for data in created_tasks])

        if updated_tasks:
            Task.objects.bulk_update(
                [Task(parent=parent_task, **data) for data in updated_tasks],
                fields=["title", "description", "parent"],
            )

    def create(self, validated_data):
        version = self.context.get("request").version
        if version > "3.0.0":
            logger.error("not supported version, take a decision you need")

        sub_tasks = validated_data.pop("sub_tasks", None)

        with transaction.atomic():
            parent_task = Task.objects.create(**validated_data)
            self.handle_sub_tasks(parent_task, sub_tasks)
            return parent_task

    def update(self, instance, validated_data):
        sub_tasks = validated_data.pop("sub_tasks", None)
        with transaction.atomic():
            for k, v in validated_data.items():
                setattr(instance, k, v)
            instance.save()

            self.handle_sub_tasks(instance, sub_tasks)

        return instance
