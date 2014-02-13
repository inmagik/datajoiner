from django.conf.urls import patterns, include, url

from .views import UserFileListView, UserFileCreateView, UserFileUpdateView
from .views import UserTaskListView, UserTaskCreateView, UserTaskUpdateView, UserTaskRunView


urlpatterns = patterns('',

    
    url(r'^userfile-list/$', UserFileListView.as_view(), name='userfile_list'),
    url(r'^userfile/$', UserFileCreateView.as_view(), name='userfile_create'),
    url(r'^userfile/(?P<pk>\d+)/$', UserFileUpdateView.as_view(), name='userfile_edit'),

    url(r'^usertask-list/$', UserTaskListView.as_view(), name='usertask_list'),
    url(r'^usertask/$', UserTaskCreateView.as_view(), name='usertask_create'),
    url(r'^usertask/(?P<pk>\d+)/$', UserTaskUpdateView.as_view(), name='usertask_edit'),
    url(r'^usertask/run/(?P<pk>\d+)/$', UserTaskRunView.as_view(), name='usertask_run'),

)

