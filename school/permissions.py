from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderators').exists()


class CanEditLessonOrCourse(IsModerator):
    def has_object_permission(self, request, view, obj):
        # Модераторам разрешено редактировать, но не создавать или удалять
        return view.action in ['retrieve', 'update', 'partial_update'] and super().has_object_permission(request, view, obj)


class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешение для модераторов
        if request.user.groups.filter(name='Moderators').exists():
            return True

        # Разрешение для владельца (пользователя, создавшего курс или урок)
        return obj.user == request.user
