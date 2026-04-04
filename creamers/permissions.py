from rest_framework import permissions

class IsPremiumUser(permissions.BasePermission):
    """
    Allows access only to users with is_premium = True.
    """
    def has_permission(self, request, view):
        # Check if user is logged in AND is marked as premium
        return bool(request.user and request.user.is_authenticated and request.user.is_premium)

class IsSeller(permissions.BasePermission):
    """
    Allows access only to users marked as Seller.
    """
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.client_status == 'Seller')