# myapp/api.py
from tastypie.resources import ModelResource
from .models import UserFile, UserFileAnnotation, UserTask
from tastypie import fields, utils
from tastypie.authentication import SessionAuthentication,Authentication
from tastypie.authorization import Authorization

import json

class UserFileAnnotationResource(ModelResource):

    result = fields.DictField(attribute='result', null=True)
    state = fields.CharField(attribute='state', null=True)
    data = fields.DictField(attribute='data', null=True)

    def get_object_list(self, request):
        obj_list = super(UserFileAnnotationResource, self).get_object_list(request)
        return obj_list.filter(userfile__user=request.user)
    

    class Meta:
        queryset = UserFileAnnotation.objects.all()
        resource_name = 'userfileannotation'

class UserFileResource(ModelResource):

    annotation = fields.ToOneField(UserFileAnnotationResource, 'annotation', full=True)

    def get_object_list(self, request):
        obj_list = super(UserFileResource, self).get_object_list(request)
        return obj_list.filter(user=request.user)

    class Meta:
        queryset = UserFile.objects.all()
        resource_name = 'userfile'


class UserTaskResource(ModelResource):


    def get_object_list(self, request):
        obj_list = super(UserTaskResource, self).get_object_list(request)
        return obj_list.filter(user=request.user)

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        bundle.obj.left_hand_data_id = bundle.data['left_hand']
        bundle.obj.right_hand_data_id = bundle.data['right_hand']
        return bundle

    class Meta:
        queryset = UserTask.objects.all()
        resource_name = 'usertask'
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

        