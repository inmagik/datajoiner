from django.db.models.fields.related import ForeignKey
from django.db.models import FileField
import uuid
import os
import zipfile

def get_uuid():
    return str(uuid.uuid1())



#helper function to convert a django model instance to a dictiornary, including ForeignKeys

def instance_dict(instance, key_format=None, recursive=False):
    "Returns a dictionary containing field names and values for the given instance"
    if key_format:
        assert '%s' in key_format, 'key_format must contain a %s'
    key = lambda key: key_format and key_format % key or key

    d = {}
    for field in instance._meta.fields:
        attr = field.name
        value = getattr(instance, attr)
        if value is not None and isinstance(field, ForeignKey):
            if not recursive:
                value = value._get_pk_val()
            else:
                value = instance_dict(value)
        if isinstance(field,FileField):
            value = value.url

        d[key(attr)] = value
    for field in instance._meta.many_to_many:
        if not recursive:
            d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
        else:
            d[key(field.name)] = [instance_dict(obj) for obj in getattr(instance, field.attname).all()]

    return d



def unzip_file(src, dst):
    with zipfile.ZipFile(src, "r") as z:
        z.extractall(dst)


def zip_file(src, dst):
    zf = zipfile.ZipFile("%s" % (dst), "w")
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            #print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                       # arcname)
            zf.write(absname, arcname)
    zf.close()