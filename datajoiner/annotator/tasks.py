from __future__ import absolute_import
from celery import shared_task
from celery.decorators import task
from annotator.core import annotator

@task
def annotate_file(obj, annotation):
    data = annotator.annotate_file(obj.data_file.path, obj.filetype)
    annotation.data = data;
    if 'content_type' in data:
        annotation.content_type = data['content_type']
    annotation.pending = False;
    annotation.save();
    return data

