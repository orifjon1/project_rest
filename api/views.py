from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer, SectorSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from users.models import CustomUser, Sector
from task.serializers import TaskSerializer, TaskReviewSerializer
from task.models import Task
from .permission import IsDirectorOrReadOnly, IsWorkerOrReadOnly, CanWriteReview


class TaskViewSet(APIView):
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['id', 'name', 'deadline', 'status']

    def get(self, request):
        tasks = Task.objects.all()
        queryset = self.filter_queryset(tasks)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset


class SectorView(APIView):
    """
    GET all sectors
    """
    def get(self, request):
        sectors = Sector.objects.all()
        serializer = SectorSerializer(sectors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    """
    Create a sector
    """
    def post(self, request):
        serializer = SectorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserView(APIView):
    """
    Get all users
    """
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    """
    Sign up 
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsDirectorOrReadOnly]
    """
    Creating a task by 'director' and 'manager'
    or
    Get all tasks
    """
    def get_queryset(self):
        return Task.objects.filter(boss=self.request.user)

    def perform_create(self, serializer):
        serializer.save(boss=self.request.user)


class TaskDisplayView(APIView):
    permission_classes = [IsAuthenticated, IsWorkerOrReadOnly]
    """
    Only workers get their tasks that are assigned from 'director' [workers are employees or managers]
    """
    def get(self, request):
        tasks = Task.objects.filter(worker=self.request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskReviewView(APIView):
    permission_classes = [CanWriteReview, IsAuthenticated]

    def get(self, request, id):
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    """
    One [who is/ assigned to/from a task] can write a review for the task
    """
    def post(self, request, id):
        user = self.request.user
        task = Task.objects.get(id=id)
        serializer = TaskReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, task=task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

