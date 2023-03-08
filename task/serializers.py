from .models import Task, TaskReview
from rest_framework import serializers
from users.serializers import UserSerializer




class TaskSerializer(serializers.ModelSerializer):
    boss = serializers.ReadOnlyField(source='self.request.user')
    remain_days = serializers.SerializerMethodField()
    all_days = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'deadline', 'boss', 'worker',
                  'remain_days', 'all_days', 'status']
        read_only_fields = ('status', 'boss')

    def get_remain_days(self, obj):
        return obj.remain_days

    def get_all_days(self, obj):
        return obj.all_days


class TaskReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = TaskReview
        fields = ['id', 'user', 'task', 'content', 'created']
        read_only_fields = ('created',)
