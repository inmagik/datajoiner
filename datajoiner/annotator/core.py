import hashlib
import os
import tablib
import chardet
import StringIO
import csv


class Annotator(object):
    
    def annotate_file(self, path, filetype):
        """
        Gets some info about a file
        """
       
        rawdata = open(path).read()
        data = self.base_annotations(path, filetype, rawdata)
        specialized_method = self.get_specialized_annotator(filetype)
        if specialized_method is not None:
            specialized_data = specialized_method(path, filetype, rawdata)
            data.update(specialized_data)


        return data

    def base_annotations(self, path, filetype, rawdata):
        out = {}
        result = chardet.detect(rawdata)
        
        charenc = result['encoding']

        out['encoding'] = charenc
        #md5
        md5 = hashlib.md5(rawdata).hexdigest()
        out['md5'] = md5
        #size
        out['size'] = os.path.getsize(path)

        return out




    def get_specialized_annotator(self, filetype, **kwargs):
        method_name = "annotate_%s" %filetype.replace("/", "_")
        return getattr(self, method_name, None)


    
    def annotate_text_csv(self, path, filetype, rawdata):
        out = {}
        out ['test'] = "csv"
        dialect = csv.Sniffer().sniff(rawdata)
        
        reader = csv.DictReader(StringIO.StringIO(rawdata), dialect=dialect)
        out['fieldnames'] = reader.fieldnames
        out['delimiter'] = dialect.delimiter
        out['quoting'] = dialect.quoting

        return out


annotator = Annotator()

