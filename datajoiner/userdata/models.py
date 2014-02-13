from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import mimetypes

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
        if not self.name:
            self.name = self.data_file.name
        return super(UserFile, self).save(*args, **kwargs)

    
    def unicode(self):
        return u'%s' % self.name




class UserTaskBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    #this is the task id in a worker
    task_id = models.CharField(max_length=100, blank=True, null=True)
    result_file = models.ForeignKey(UserFile, related_name="tasks_results", null=True, blank=True, editable=False)

    class Meta:
        abstract = True


class UserTask(UserTaskBase):
    
    left_hand_data = models.ForeignKey(UserFile, related_name="tasks_left")
    right_hand_data = models.ForeignKey(UserFile, related_name="tasks_right")
    left_hand_field = models.CharField(max_length=100)
    right_hand_field = models.CharField(max_length=100, blank=True, null=True)



