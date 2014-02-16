import hashlib
import os
import tablib
import chardet
import StringIO
import csv
from django.conf import settings
import os
import shutil
import shapefile

from inmagik_utils.helpers import zip_file, unzip_file

ANNOTATOR_WORKDIR = os.path.join(settings.MEDIA_ROOT, "annotations")
if not os.path.isdir(ANNOTATOR_WORKDIR):
    os.mkdir(ANNOTATOR_WORKDIR)


class Annotator(object):
    
    def annotate_file(self, path, filetype):
        """
        Gets some info about a file
        """
        
        data = self.base_annotations(path, filetype)
        specialized_method = self.get_specialized_annotator(filetype)
        
        if specialized_method is not None:
            specialized_data = specialized_method(path, filetype)
            data.update(specialized_data)
        return data


    def get_folder(self, path):
        basename = os.path.basename(path)
        fullname = os.path.join(ANNOTATOR_WORKDIR, basename)
        try:
            shutil.rmtree(fullname)
        except:
            pass
        os.mkdir(fullname)
        return fullname


    def base_annotations(self, path, filetype):
        out = { 'mimetype' : filetype}
        #size
        out['size'] = os.path.getsize(path)

        return out


    def get_content_annotations(self, rawdata):
        out = { }
        #encoding
        result = chardet.detect(rawdata)
        charenc = result['encoding']
        
        if charenc=="ISO-8859-2":
            charenc="latin-1"
        if charenc=="ascii":
            charenc="utf-8"
            
        out['encoding'] = charenc
        #md5
        md5 = hashlib.md5(rawdata).hexdigest()
        out['md5'] = md5

        return out  


    def get_specialized_annotator(self, filetype, **kwargs):
        method_name = "annotate_%s" %filetype.replace("/", "_")
        return getattr(self, method_name, None)


    
    def annotate_text_csv(self, path, filetype):
        out = {}
        out ['main_file'] = path
        out ['content_type'] = 'csv'
        rawdata = open(path).read()
        dialect = csv.Sniffer().sniff(rawdata)
        reader = csv.DictReader(StringIO.StringIO(rawdata), dialect=dialect)
        
        out['fieldnames'] = reader.fieldnames
        out['delimiter'] = dialect.delimiter
        out['quoting'] = dialect.quoting
        
        out.update(self.get_content_annotations(rawdata))
        return out


    def annotate_application_zip(self, path, filetype):
        out = {}
        out ['main_file'] = path
        #unzip it somewhere
        unzip_path = self.get_folder(path)
        unzip_file(path, unzip_path)
        
        #check for shapefile
        out.update(self.check_for_shapefile(unzip_path))

        return out

    def check_for_shapefile(self, path):
        out  = { 'shapefile' : None }
        #TODO:.prj should be there?
        must_get = ['.shp', '.dbf']
        
        for filename in os.listdir(path):
            for item in [x for x in must_get]:
                if filename.endswith(item):
                    must_get.remove(item)
                    if item == '.shp': 
                        out['shapefile'] = os.path.join(path, filename)

        if not len(must_get):
            out['content_type'] = 'shapefile'
            source_shape = shapefile.Reader(out['shapefile'])
            source_fields  = list(source_shape.fields[1:])
            out['fieldnames'] = [x[0] for x in source_fields]
            return out

        return {}




annotator = Annotator()

