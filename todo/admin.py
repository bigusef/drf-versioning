from django.contrib import admin

from .models import Task


class TaskTabularInline(admin.TabularInline):
    model = Task
    fk_name = 'parent'
    extra = 1


@admin.register(Task)
class TaskModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "view_sub_tasks_count", "created_at", "last_modified"]
    inlines = [TaskTabularInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent__isnull=True)

    @admin.display(description="sub tasks count")
    def view_sub_tasks_count(self, obj):
        return obj.sub_tasks.count()
