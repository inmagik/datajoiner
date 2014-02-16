from django.conf.urls import patterns, include, url

from .views import UserFileListView, UserFileCreateView, UserFileUpdateView, UserFileDetailView, UserFileDeleteView
from .views import UserTaskListView, UserTaskCreateView, UserTaskUpdateView, UserTaskRunView, TaskInfo


from .api import UserFileResource,UserFileAnnotationResource

userfile_resource = UserFileResource()
userfileannotation_resource = UserFileAnnotationResource()

urlpatterns = patterns('',

    
    url(r'^userfile-list/$', UserFileListView.as_view(), name='userfile_list'),
    url(r'^userfile/$', UserFileCreateView.as_view(), name='userfile_create'),
    url(r'^userfile/detail/(?P<pk>\d+)/$', UserFileDetailView.as_view(), name='userfile_detail'),
    url(r'^userfile/delete/(?P<pk>\d+)/$', UserFileDeleteView.as_view(), name='userfile_delete'),
    url(r'^userfile/(?P<pk>\d+)/$', UserFileUpdateView.as_view(), name='userfile_edit'),

    url(r'^usertask-list/$', UserTaskListView.as_view(), name='usertask_list'),
    url(r'^usertask/$', UserTaskCreateView.as_view(), name='usertask_create'),
    url(r'^usertask/(?P<pk>\d+)/$', UserTaskUpdateView.as_view(), name='usertask_edit'),
    url(r'^usertask/run/(?P<pk>\d+)/$', UserTaskRunView.as_view(), name='usertask_run'),


    url(r'^taskinfo/(?P<task_id>(\w|-)+)/$', TaskInfo.as_view(), name='task_info'),

    (r'^api/', include(userfile_resource.urls)),
    (r'^api/', include(userfileannotation_resource.urls)),


)

