from django.conf.urls import patterns, include, url
from .views import IndexView, JoinWidgetView #,UserFilesView

urlpatterns = patterns('',
    
    #url(r'^admin/', include("ui.urls")),
    url(r'^join-widget/$', JoinWidgetView.as_view(), name="join_widget"),
    url(r'^$', IndexView.as_view(), name="home"),
    

    #url(r'^userfiles', UserFilesView.as_view(), name="home"),

)
