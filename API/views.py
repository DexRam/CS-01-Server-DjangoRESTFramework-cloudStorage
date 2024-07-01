from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, File
from .serializers import UserSerializer, FileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            serializer = self.get_serializer(user)
            data = serializer.data
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

