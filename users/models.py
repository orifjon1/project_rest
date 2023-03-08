from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import Help
from datetime import datetime
from task.models import Task


class Sector(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
   Status = (('director', 'Director'),
              ('manager', 'Manager'),
              ('employee', 'Employee'),)
   status = models.CharField(max_length=15, choices=Status, default='employee')
   sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True, blank=True)

   def __str__(self):
       return self.username


class DirectorProfile(Help):
    director = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.director.__str__()


class EmployeeProfile(Help):
    employee = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='e_task_stats',
                                    limit_choices_to={'user_type': 'employee'})
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='employees')
    tasks_finished = models.PositiveIntegerField(default=0)
    tasks_doing = models.PositiveIntegerField(default=0)
    tasks_canceled = models.PositiveIntegerField(default=0)
    tasks_missed_deadline = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.employee.__str__()

    def update_task_stats(self):
        self.tasks_finished = Task.objects.filter(worker=self.employee, status='done').count()
        self.tasks_doing = Task.objects.filter(worker=self.employee, status='doing').count()
        self.tasks_canceled = Task.objects.filter(worker=self.employee, status='canceled').count()
        self.tasks_missed_deadline = Task.objects.filter(worker=self.employee, status='todo',
                                                         deadline__lt=datetime.now()).count()
        self.save()


class ManagerProfile(Help):
    manager = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='m_task_stats',
                                   limit_choices_to={'user_type': 'manager'})
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='managers')
    tasks_finished = models.PositiveIntegerField(default=0)
    tasks_doing = models.PositiveIntegerField(default=0)
    tasks_canceled = models.PositiveIntegerField(default=0)
    tasks_missed_deadline = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.manager.__str__()

    def update_task_stats(self):
        self.tasks_finished = Task.objects.filter(worker=self.manager, status='done').count()
        self.tasks_doing = Task.objects.filter(worker=self.manager, status='doing').count()
        self.tasks_canceled = Task.objects.filter(worker=self.manager, status='canceled').count()
        self.tasks_missed_deadline = Task.objects.filter(worker=self.manager, status='todo',
                                                         deadline__lt=datetime.now()).count()
        self.save()
