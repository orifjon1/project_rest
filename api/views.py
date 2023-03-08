from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer, SectorSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser, Sector
from task.serializers import TaskSerializer, TaskReviewSerializer
from task.models import Task
from .permission import IsDirectorOrReadOnly, IsWorkerOrReadOnly, CanWriteReview


class SectorView(APIView):
    def get(self, request):
        sectors = Sector.objects.all()
        serializer = SectorSerializer(sectors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SectorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TaskView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsDirectorOrReadOnly]

    def get_queryset(self):
        return Task.objects.filter(boss=self.request.user)

    def perform_create(self, serializer):
        serializer.save(boss=self.request.user)


class TaskWorkerView(APIView):
    permission_classes = [IsAuthenticated, IsWorkerOrReadOnly]

    def get(self, request):
        tasks = Task.objects.filter(worker=self.request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

#     def post(self, request):
#
#         serializer = TaskSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(boss=self.request.user)
#         return Response(serializer.data)


class TaskReviewView(APIView):
    permission_classes = [CanWriteReview, IsAuthenticated]

    def get(self, request, id):
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def post(self, request, id):
        user = self.request.user
        task = Task.objects.get(id=id)
        serializer = TaskReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, task=task)
        return Response(serializer.data)
