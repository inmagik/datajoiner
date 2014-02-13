from django import forms
from itsdangerous import TimestampSigner
from django.conf import settings
from django.core.urlresolvers import reverse
from emailuser.models import EmailUser
from .helpers import send_template_email
from django.utils.translation import ugettext_lazy as _

SECRET_KEY = settings.SIGNING_KEY



class RegistrationForm(forms.Form):
    email = forms.EmailField(label=_("Email address"))
    
    def clean_email(self):
        data = self.cleaned_data['email']
        
        try:
            user = EmailUser.objects.get(email=data)
        except:
            user = None
        
        if user:
            raise forms.ValidationError(_("Email already registered"))
        
        return data


    def send_email(self, host):
        # send email using the self.cleaned_data dictionary
        data = self.cleaned_data
        email = data['email']

        s = TimestampSigner(SECRET_KEY, salt="register-user")
        token_string = s.sign(email)
        registration_url = reverse('activate_user')
        registration_url += "?em_tk=" + token_string
        #registration_url = PRODUCTION_BASE_URL + registration_url
        registration_url = "http://" +  host + registration_url
        
        ctx = { 'email' : email, 'registration_url' : registration_url }
        send_template_email(_("Email verification for signup"), "verified_registration/registration_mail.html", ctx, email)


class ChangePasswordForm(forms.Form):
    email = forms.EmailField(label=_("Email address"))
    
    def clean_email(self):
        data = self.cleaned_data['email']
        
        try:
            user = EmailUser.objects.get(email=data)
        except:
            raise forms.ValidationError(_("Wrong email"))
        
        return data


    def send_email(self):
        # send email using the self.cleaned_data dictionary
        data = self.cleaned_data
        email = data['email']

        s = TimestampSigner(SECRET_KEY, salt="change-password")
        token_string = s.sign(email)
        registration_url = reverse('change_password')
        registration_url += "?em_tk=" + token_string
        #registration_url =PRODUCTION_BASE_URL + registration_url
        registration_url = "http://" +  host + registration_url

        ctx = { 'email' : email, 'registration_url' : registration_url }
        send_template_email(_("Reset password confirmation"), "verified_registration/password_recover_mail.html", ctx, email)

        
        