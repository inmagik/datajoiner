from django.conf.urls import patterns, include, url
from .views import IndexView #,UserFilesView

urlpatterns = patterns('',
    
    #url(r'^admin/', include("ui.urls")),
    url(r'^$', IndexView.as_view(), name="home"),
    #url(r'^userfiles', UserFilesView.as_view(), name="home"),

)
