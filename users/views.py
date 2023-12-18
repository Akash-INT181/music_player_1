from rest_framework import viewsets, status
from .serializers import RegisterUserSerializer, UserSerializer
from rest_framework.views import APIView

from .models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        password = self.request.data.get("password")
        user = serializer.save()
        user.set_password(password)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def perform_update(self, serializer):
        password = self.request.data.get("password")
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserRegistrationView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        # print(serializer.is_valid(), serializer.data)

        if serializer.is_valid():
            data = serializer.data
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
            )
            user.set_password(data["password"])
            user.save()
            return Response({"user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
