from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super(UserViewSet, self).get_permissions()

