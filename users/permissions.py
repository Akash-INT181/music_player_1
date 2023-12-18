# permissions.py
from rest_framework import permissions


# class IsOwnerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         print("Checking permissions:")
#         print(f"Object ID: {obj.id}")
#         print(f"User ID: {request.user.id}")

#         # Allow read access to any authenticated user.
#         if request.method in permissions.SAFE_METHODS:
#             print("Allowing read access.")
#             return True

#         # Allow write access only if the user is the owner of the object.
#         if obj.id == request.user.id:
#             print("Allowing write access.")
#             return True

#         print("Denying access.")
#         return False
