from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'datajoiner.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^verified_registration/', include('verified_registration.urls')),
    url (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^data/', include("userdata.urls")),
    url(r'^', include("ui.urls")),

)

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)