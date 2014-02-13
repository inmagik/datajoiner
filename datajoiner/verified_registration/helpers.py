from django.template import Context, Template
from django.template.loader import get_template
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_template_email(subject, template, ctx, to, from_email=None):
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL

    t = get_template(template)
    c = Context(ctx)
    html_content = t.render(c)

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()