from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404
from django import forms

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse, reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic.base import TemplateView

from itsdangerous import TimestampSigner
import itsdangerous
from django.conf import settings

SECRET_KEY = settings.SIGNING_KEY
MAX_TOKEN_AGE = settings.MAX_TOKEN_AGE 


from .forms import RegistrationForm, ChangePasswordForm
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView
from emailuser.models import EmailUser
from emailuser.forms import EmailUserCreationForm
from django.forms import ValidationError

from django.contrib.auth import authenticate, logout, login



class RegistrationView(FormView):
    template_name = 'verified_registration/registration.html'
    form_class = RegistrationForm
    
    def get_success_url(self):
        return reverse('register_success')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        host = self.request.META['HTTP_HOST']
        form.send_email(host)
        return super(RegistrationView, self).form_valid(form)


class RegistrationSuccessView(TemplateView):
    template_name = "verified_registration/registration_success.html"


from django.utils.safestring import mark_safe
#tr_dati_href = '/trattamento-dati'
#LINK_TRATTAMENTO_DATI = '<a href="%s" target="_blank">terms of service</a>' %  tr_dati_href



class RegistrationPasswordOnlyForm(EmailUserCreationForm):
    

    def __init__(self, *args, **kwargs):
        super(RegistrationPasswordOnlyForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True

    def clean_password1(self):
        password = self.cleaned_data['password1']
        if(len(password) < 8):
            raise ValidationError('Password must be at least 8 characters long')

        return password

class RegistrationPasswordAndConfirmForm(RegistrationPasswordOnlyForm):
    confirm = forms.BooleanField(label=mark_safe('Accept terms of service...'), required=False)

    def __init__(self, *args, **kwargs):
        super(RegistrationPasswordAndConfirmForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
    
    def clean_confirm(self,*args,**kwargs):
        confirmation = self.cleaned_data['confirm']
        if not confirmation:
            raise ValidationError('You must accept terms of service')

        return confirmation
    


class RegistrationActionView(CreateView):
    model = EmailUser
    form_class=RegistrationPasswordAndConfirmForm
    template_name = "verified_registration/user_create.html"


    def __init__(self, *args, **kwargs):
        self.email_address = None
        return super(RegistrationActionView, self).__init__(*args, **kwargs)
    
    def dispatch(self, *args, **kwargs):
        if "em_tk" not in self.request.GET:
            return HttpResponseRedirect(reverse('home'))

        email_token =  self.request.GET.get('em_tk')
        s = TimestampSigner(SECRET_KEY, salt="register-user")
        try:
            self.email_address = s.unsign(email_token, max_age=MAX_TOKEN_AGE)
        except: #itsdangerous.BadSignature:
            raise Http404
            #return HttpResponseRedirect(reverse('home'))


        return super(RegistrationActionView, self).dispatch(*args, **kwargs)

    
    def get_initial(self):
        return { 'email': self.email_address }


    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        out = super(RegistrationActionView, self).form_valid(form)
        if getattr(settings, 'LOGIN_AFTER_REGISTER', False):
            self.object.backend = "django.contrib.auth.backends.ModelBackend"
            login(self.request, self.object)
        return out


    def get_success_url(self):
        if getattr(settings, 'LOGIN_AFTER_REGISTER', False):
            return settings.REGISTER_REDIRECT_URL
        return settings.LOGIN_REDIRECT_URL    


class PasswordChangeView(UpdateView):
    model = EmailUser
    form_class=RegistrationPasswordOnlyForm
    template_name = "verified_registration/change_password.html"


    def __init__(self, *args, **kwargs):
        self.email_address = None
        return super(PasswordChangeView, self).__init__(*args, **kwargs)
    
    

    def dispatch(self, *args, **kwargs):
        if "em_tk" not in self.request.GET:
            return HttpResponseRedirect(reverse('home'))

        email_token =  self.request.GET.get('em_tk')
        s = TimestampSigner(SECRET_KEY,salt="change-password")
        try:
            self.email_address = s.unsign(email_token, max_age=MAX_TOKEN_AGE)
        except:# itsdangerous.BadSignature:
            raise Http404
            #return HttpResponseRedirect(reverse('home'))

        return super(PasswordChangeView, self).dispatch(*args, **kwargs)


    def get_object(self, *args, **kwargs):
        return EmailUser.objects.get(email=self.email_address )

    
    def get_initial(self):
        return { 'email': self.email_address }


    def get_success_url(self):
        return reverse('login')

class PasswordSentSuccessView(TemplateView):
    template_name = "verified_registration/password_send_success.html"

    
class PasswordResetView(FormView):
    template_name = 'verified_registration/password_reset.html'
    form_class = ChangePasswordForm
    
    def get_success_url(self):
        return reverse('password_send_success')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        host = self.request.META['HTTP_HOST']
        form.send_email(host)
        return super(PasswordResetView, self).form_valid(form)