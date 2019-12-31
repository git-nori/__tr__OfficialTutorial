from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission
    snippetの作成者のみ更新、削除が行えるようにする
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS => GET, HEAD or OPTIONS requests
            return True
        return obj.owner == request.user
