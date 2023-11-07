from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=75)
    description = models.TextField()
    parent = models.ForeignKey("Task", on_delete=models.CASCADE, null=True, blank=True, related_name="sub_tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
