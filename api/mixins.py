from rest_framework import permissions

from .permissions import DjangoModelPermission


class UserPermissionMixin():
    permission_classes = [DjangoModelPermission]


class AdminPermissionMixin():
    permission_classes = [permissions.IsAdminUser, DjangoModelPermission]