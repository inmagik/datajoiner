from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import mimetypes
from jsonfield import JSONField
from inmagik_utils.helpers import get_uuid
from celery.result import AsyncResult




class UserFileBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=True)
    data_file = models.FileField(upload_to="data_files")
    filetype = models.CharField(max_length=100, null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        mime = mimetypes.guess_type(self.data_file.path)
        self.filetype = mime[0]
        return super(UserFileBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True



class UserFile(UserFileBase):

    name = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        #setting name automatically if not given
        #if not self.name:
        self.name = self.data_file.name
        return super(UserFile, self).save(*args, **kwargs)

    
    def get_main_path(self):
        return self.data_file.path


    def __unicode__(self):
        return u'%s' % self.name





class ModelWithTask(models.Model):
    task_id = models.CharField(max_length=100, blank=True, null=True, editable=False)
    @property
    def state(self):
        if not self.task_id:
            return None
        task = AsyncResult(self.task_id)
        return task.state

    
    @property
    def result(self):
        if not self.task_id:
            return None
        task = AsyncResult(self.task_id)
        return task.result
        


    class Meta:
        abstract = True

class UserTaskBase(ModelWithTask):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    result_file = models.ForeignKey(UserFile, related_name="tasks_results", null=True, blank=True, editable=False,
        on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class UserFileAnnotation(ModelWithTask):
    """
    must be re(generated) when a userfile is saved
    """
    userfile = models.OneToOneField(UserFile, related_name="annotation")
    data = JSONField(null=True, blank=True)
    pending = models.BooleanField(default=False, editable=False)

    def __unicode__(self):
        return u'%s' % self.task_id


    @property
    def state(self):
        if self.pending or not self.task_id:
            return None
        task = AsyncResult(self.task_id)
        return task.state

    
    @property
    def result(self):
        if self.pending or not self.task_id:
            return None
        task = AsyncResult(self.task_id)
        return task.result



class UserTask(UserTaskBase):
    
    left_hand_data = models.ForeignKey(UserFile, related_name="tasks_left")
    right_hand_data = models.ForeignKey(UserFile, related_name="tasks_right")
    left_hand_field = models.CharField(max_length=100)
    right_hand_field = models.CharField(max_length=100, blank=True, null=True)






from django.core.signals import request_finished
from django.dispatch import receiver
#from django.core.signals import request_finished
from django.db.models.signals import post_save, post_delete
from annotator.tasks import annotate_file

@receiver(post_save, sender=UserFile)
def update_annotation(sender, **kwargs):
    obj = kwargs['instance']
    try:
        annotation = UserFileAnnotation.objects.get(userfile=obj)
    except UserFileAnnotation.DoesNotExist, e:
        annotation = UserFileAnnotation.objects.create(userfile=obj)

    task_id = get_uuid()
    annotation.pending = True
    annotation.task_id = task_id
    annotation.save()
    annotate_file.apply_async((obj, annotation), task_id=task_id)
    
    

@receiver(post_delete, sender=UserFile)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.data_file.delete(False)




