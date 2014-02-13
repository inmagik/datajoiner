from django.conf.urls import patterns, include, url


from .views import ( RegistrationView, PasswordSentSuccessView,
        RegistrationSuccessView, RegistrationActionView, PasswordChangeView, PasswordResetView)

urlpatterns = patterns('',
    # Examples:
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name':'verified_registration/login.html'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}, name="logout"),
    url(r'^act_us/$', RegistrationActionView.as_view(), name="activate_user"),
    url(r'^res_pwd/$', PasswordChangeView.as_view(), name="change_password"),
    url(r'^register_success/$', RegistrationSuccessView.as_view(), name="register_success"),
    url(r'^register/$', RegistrationView.as_view(), name="register"),    
    url(r'^ask_reset/$', PasswordResetView.as_view(), name="password_reset"),
    url(r'^password_send_success/$', PasswordSentSuccessView.as_view(), name="password_send_success"),

)
