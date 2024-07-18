import os
from django.http import FileResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import get_object_or_404

from .models import User, File
from .serializers import UserSerializer, FileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(user)
        serializer = self.get_serializer(user)
        data = serializer.data
        data.update({"refresh": str(refresh), "access": str(refresh.access_token)})
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(
        detail=False,
        methods=["post"],
        url_path="upload-file",
        permission_classes=[IsAuthenticated],
    )
    def upload_file(self, request, *args, **kwargs):
        print(request.data)
        user = request.user
        user_id = request.data.get("id")
        if user.is_admin and user_id:
            user_to_create = get_object_or_404(User, id=user_id)
        else:
            user_to_create = user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=user_to_create)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["patch"],
        url_path="update-file",
        permission_classes=[IsAuthenticated],
    )
    def update_file(self, request, pk=None):
        file_instance = self.get_object()
        serializer = self.get_serializer(file_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        url_path="download-file",
        permission_classes=[IsAuthenticated],
    )
    def download_file(self, request, pk=None):
        file_instance = self.get_object()
        if not (request.user == file_instance.owner or request.user.is_admin):
            return Response(
                {"Error": "You do not have permission to access this file."},
                status=status.HTTP_403_FORBIDDEN,
            )

        file_path = file_instance.file.path
        file_name = file_instance.file.name
        file = open(file_path, "rb")
        response = FileResponse(file, as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response

    @action(
        detail=True,
        methods=["post"],
        url_path="share-file",
        permission_classes=[IsAuthenticated],
    )
    def share_file(self, request, pk=None):
        file_instance = self.get_object()
        if not (request.user == file_instance.owner or request.user.is_admin):
            return Response(
                {"Error": "You do not have permission to access this file."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not file_instance.share_link:
            file_instance.share_link = file_instance.generate_share_link()
        else:
            file_instance.share_link = ""
        file_instance.save()
        serializer = self.get_serializer(file_instance)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["delete"],
        url_path="delete-file",
        permission_classes=[IsAuthenticated],
    )
    def delete_file(self, request, *args, **kwargs):
        file_instance = self.get_object()
        if not (request.user == file_instance.owner or request.user.is_admin):
            return Response(
                {"Error": "You do not have permission to access this file."},
                status=status.HTTP_403_FORBIDDEN,
            )
        file_instance.file.delete()
        file_instance.delete()
        return Response(
            {"message": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="user-files",
        permission_classes=[IsAuthenticated],
    )
    def user_files(self, request):
        user = request.user
        user_id = request.data.get("id")
        if user.is_admin and user_id:
            files = File.objects.filter(owner=user_id)
        else:
            files = File.objects.filter(owner=user)
        serializer = self.get_serializer(files, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="download-shared/(?P<share_link>[^/.]+)",
        permission_classes=[AllowAny],
    )
    def download_shared(self, request, share_link=None):
        file_instance = get_object_or_404(File, share_link=share_link)
        file_path = file_instance.file.path
        file_name = file_instance.file.name
        file = open(file_path, "rb")
        response = FileResponse(file, as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response
