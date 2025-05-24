from rest_framework.permissions import BasePermission

class EventPermission(BasePermission):
  """
  - Admin has all access.
  - All user can perform get request.
  - Authenticated user can perform post request.
  - Creators can edit their own objects, with restrictions on modifying certain fields (is_approved).
  """
  def has_permission(self, request, view):
    # Allow all user for get request
    if request.method == 'GET':
      return True
    # Allow POST request for authenticated user
    if request.user.is_authenticated and request.method == 'POST':
      return True
    if request.user.is_staff:
      return True
    return False
  
  def has_object_permission(self, request, view, obj):
    # Allow admin to have all permission
    if request.user.is_staff:
      return True
    # Allow creator to edit the content
    if obj.created_by == request.user:
      if request.method in ['PUT', 'PATCH']:
        if 'is_approved' in request.data:
          return False
      return True
    
    return False