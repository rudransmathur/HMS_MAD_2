from celery import shared_task

@shared_task
def add_func(a,b):
    return a+b