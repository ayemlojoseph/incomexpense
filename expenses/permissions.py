from rest_framework import permissions

#this will enable only the created user to view the expenses so another
#user wont be able to view someonelse records

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user 
        #this means the onwner of the object trying to be accessed must be
        # the same with the user requesting the access
