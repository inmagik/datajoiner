from __future__ import absolute_import
from celery import shared_task
from celery.decorators import task
from annotator.core import annotator

@task
def annotate_file(obj, annotation):
    data = annotator.annotate_file(obj.data_file.path, obj.filetype)
    annotation.data = data;
    annotation.pending = False;
    annotation.task_id = annotate_file.request.id
    annotation.save();

    print "xxxx", annotation.task_id
    return data

