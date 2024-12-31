from rest_framework import generics, permissions
from .serializers import UserSerializer



class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    
    def get_object(self):
        return self.request.user