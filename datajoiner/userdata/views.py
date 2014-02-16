from django.shortcuts import render
from django.core.urlresolvers import reverse

from django.views.generic import ListView, View, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django import forms
from django.utils.translation import ugettext_lazy as _
from inmagik_utils.views import LoginRequiredMixin, AjaxableResponseMixin

from .models import UserFile, UserTask
from celery.result import AsyncResult
from django.http import HttpResponseRedirect
from inmagik_utils.helpers import get_uuid


class UserFileForm(forms.ModelForm):
    class Meta:
        model = UserFile
        
        widgets = {
            'user' : forms.HiddenInput(),
        }
    
    class Media:
        js = ['js/datessetup.js']


class UserFileListView(LoginRequiredMixin, ListView):
    model = UserFile
    def get_queryset(self):
        qset = super(UserFileListView,self).get_queryset()
        return qset.select_related('annotation')#.filter(user=self.request.user)


class UserFileCreateView(LoginRequiredMixin, CreateView):
    model = UserFile
    form_class = UserFileForm

    def get_success_url(self):
        return reverse('userfile_list')
    def get_initial(self):
        return { 
            'user': self.request.user 
        }

    def get_context_data(self,*args,**kwargs):
        ctx = super(UserFileCreateView,self).get_context_data(*args,**kwargs)
        ctx['title'] = _("Add File")
        return ctx


class UserFileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserFile
    form_class = UserFileForm

    def get_success_url(self):
        return reverse('userfile_list')

    def get_initial(self):
        return { 
            'user': self.request.user 
        }

    def get_context_data(self,*args,**kwargs):
        ctx = super(UserFileUpdateView,self).get_context_data(*args,**kwargs)
        ctx['title'] = _("Edit File")
        return ctx


class UserFileDetailView(LoginRequiredMixin, DetailView):
    model = UserFile


class UserFileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserFile
    def get_success_url(self):
        return reverse('userfile_list')



class UserTaskForm(forms.ModelForm):
    class Meta:
        model = UserTask
        
        widgets = {
            'user' : forms.HiddenInput(),
        }
    
    class Media:
        js = ['js/datessetup.js']


class UserTaskListView(LoginRequiredMixin, ListView):
    model = UserTask
    def get_queryset(self):
        qset = super(UserTaskListView,self).get_queryset()
        return qset.filter(user=self.request.user)


class UserTaskCreateView(LoginRequiredMixin, CreateView):
    model = UserTask
    form_class = UserTaskForm

    def get_success_url(self):
        return reverse('usertask_list')
    def get_initial(self):
        return { 
            'user': self.request.user 
        }

    def get_context_data(self,*args,**kwargs):
        ctx = super(UserTaskCreateView,self).get_context_data(*args,**kwargs)
        ctx['title'] = _("Add Task")
        return ctx


class UserTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = UserTask
    form_class = UserTaskForm

    def get_success_url(self):
        return reverse('usertask_list')

    def get_initial(self):
        return { 
            'user': self.request.user 
        }

    def get_context_data(self,*args,**kwargs):
        ctx = super(UserTaskUpdateView,self).get_context_data(*args,**kwargs)
        ctx['title'] = _("Edit Task")
        return ctx


from .join_operations import join_files
from .tasks import join_files_task
#This is not fine, use celery :)
class UserTaskRunView(LoginRequiredMixin, AjaxableResponseMixin, DetailView):
    model = UserTask
    always_json = False
    template_name = "userdata/task_run.html"

    def get_context_data(self, **kwargs):
        o =  self.object
        task_id = get_uuid()
        self.object.task_id = task_id
        self.object.save()
        join_files_task.apply_async([o], task_id=task_id)
        ctx = super(UserTaskRunView,self).get_context_data(**kwargs)

    def render_to_response(self, context, **kwargs):
        return HttpResponseRedirect(reverse('usertask_list'))

    
class TaskInfo(AjaxableResponseMixin, View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs['task_id']
        task = AsyncResult(task_id)
        result = task.result
        error = None
        traceback = None
        if isinstance(result, Exception):
            error  = str(result)
            result = None
            traceback = task.traceback

        context = { 'task_id' : task_id, 'state' : task.state, 'result' : result, 'error': error, 'traceback' : traceback }
        return self.render_to_json_response(context)
    


