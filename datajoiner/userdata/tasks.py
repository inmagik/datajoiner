from __future__ import absolute_import
from celery import shared_task
from celery.decorators import task

from userdata.join_operations import join_files



@shared_task
def add(x, y):
    return x + y


@shared_task
def join_files_task(o):
    return join_files(o)

