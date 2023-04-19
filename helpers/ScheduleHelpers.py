import asyncio

from asgiref.sync import sync_to_async, async_to_sync
from django_q.models import Schedule

from service_routine.models import ServiceM


def schedule_my_task(future):
    return Schedule.objects.create(func='tg_routine.main.task_handler',
                            schedule_type='O',
                            next_run=future,
                            repeats=1,
                            )
@sync_to_async
def get_my_reminders(chat):
    service_objects = ServiceM.objects.filter(chat=chat.id)
    service_objects_schedules = {}
    for obj in service_objects:
        schedule_obj = obj.schedule
        if not schedule_obj.success():
            internal_obj = {
                'request': obj.request,
                'schedule': obj.schedule
            }
            service_objects_schedules[obj.id] = internal_obj
    return service_objects_schedules

@sync_to_async
def async_to_schedule(chat, future, request):
    scheduled_obj = schedule_my_task(future)

    ServiceM.objects.create(chat=chat,schedule=scheduled_obj, request=request)
    print("Try to exec!")

    print("Woke up after execution!")