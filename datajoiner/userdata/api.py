# myapp/api.py
from tastypie.resources import ModelResource
from .models import UserFile, UserFileAnnotation
from tastypie import fields, utils

class UserFileAnnotationResource(ModelResource):

    result = fields.DictField(attribute='result', null=True)
    state = fields.CharField(attribute='state', null=True)

    def get_object_list(self, request):
        obj_list = super(UserFileAnnotationResource, self).get_object_list(request)
        return obj_list.filter(user=request.user)
    

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