import json

from django.http import HttpResponse, Http404
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, FormMixin
from django.views.generic.list import ListView, BaseListView
from django.views.generic.base import TemplateResponseMixin
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .helpers import instance_dict



class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)



class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
     ---- Not quite true -> Must be used with an object-based FormView (e.g. CreateView)
    

    """
    always_json = False

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context, cls=DjangoJSONEncoder)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)


    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax() or self.always_json:
            return self.render_to_json_response(context, **response_kwargs)
        else:
            return super(AjaxableResponseMixin, self).render_to_response(context, **response_kwargs)


    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = instance_dict(self.object)
            return self.render_to_json_response(data)
        else:
            return response