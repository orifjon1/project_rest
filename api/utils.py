from users.models import CustomUser
from django.db.models import Count, Case, When, IntegerField, F


employee_query = CustomUser.objects.annotate(
            total_tasks=Count('accepted_tasks'),
            done_tasks=Count(Case(When(accepted_tasks__status='doing', then=1)), output_field=IntegerField()),
            finished_tasks=Count(Case(When(accepted_tasks__status='finished', then=1)), output_field=IntegerField()),
            canceled_tasks=Count(Case(When(accepted_tasks__status='canceled', then=1)), output_field=IntegerField()),
        ).annotate(
        done_tasks_percentage=100.0 * F('done_tasks') / F('total_tasks'),
        finished_tasks_percentage=100.0 * F('finished_tasks') / F('total_tasks'),
        canceled_tasks_percentage=100.0 * F('canceled_tasks') / F('total_tasks'),
    ).exclude(status='director')
