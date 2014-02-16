import mimetypes 
import csv
import tempfile
import StringIO
from django.core.files import File 
from .models import UserFile
from django.core.files.storage import default_storage
import codecs
import shapefile
import os
from inmagik_utils.helpers import zip_file, unzip_file


def join_files(o):
    left_hand = o.left_hand_data
    right_hand = o.right_hand_data
    left_hand_field = o.left_hand_field
    
    right_hand_field= o.right_hand_field
    if not right_hand_field:
        right_hand_field = left_hand_field
 

    resource_left = get_iterable_resource(left_hand.data_file.path, left_hand.annotation.data)
    resource_right = get_iterable_resource(right_hand.data_file.path, right_hand.annotation.data)

    fieldnames = resource_left.fieldnames + [x for x in resource_right.fieldnames if x not in resource_left.fieldnames]

    reader_left = resource_left.get_reader()
    reader_right = resource_right.get_reader()
    
    
    lookup_dict = {}
    for row in reader_right:
        #only first occurrence is kept
        if row[right_hand_field] not in lookup_dict:
            lookup_dict[str(row[right_hand_field])] = row

    out_rows = []    
    #scan all rows in the left and lookup on the dict, based on left_hand field
    for row in reader_left:
        lookup_value = str(row[left_hand_field])
        if lookup_value in lookup_dict:
            joint_row = lookup_dict[lookup_value]
            row.update(joint_row.item)
            
        out_rows.append(row)

    stream = resource_left.get_stream()
    resource_left.write_to_stream(out_rows, fieldnames, stream)

    if o.result_file:
        o.result_file.delete()
    
    new_name = resource_left.get_new_filename()
    path = default_storage.get_available_name(new_name)

    out_file = UserFile(user=left_hand.user)
    out_file.data_file.save(
        path,
        File(stream)
    )
    out_file.save()

    #saving result file
    o.result_file = out_file
    o.save()

    return out_file.data_file.path




def get_iterable_resource(path, data):
    mime = mimetypes.guess_type(path)
    mime = mime[0]
    if mime == "text/csv":
        return CsvResource(path, data)


    if mime == "application/zip":
        if 'shapefile' in data and data['shapefile'] is not None:
            return ShapeResource(data)


class DictRow(object):
    def __init__(self, wrapped):
        self._wrapped = wrapped
        
    @property
    def item(self):
        return self._wrapped

    def __getitem__(self, name):
        return self._wrapped[name]

    def update(self, data):
        self.item.update(data)    
        return self.item


class CsvResource(object):
    def __init__(self, path, data):
        self.path = path
        self.data = data
        self.fieldnames = self.data['fieldnames']
        
        self.dialect = None


    def get_reader(self):
        stream = open(self.path)
        dialect = csv.Sniffer().sniff(stream.read())
        stream.seek(0)
        reader = csv.DictReader(stream, dialect=dialect)
        self.dialect = dialect
        
        for row in reader:
            yield DictRow(row)


    def get_stream(self):
        stream = StringIO.StringIO()
        return stream


    def write_to_stream(self, rows, fieldnames, stream):
        writer = csv.DictWriter(stream, fieldnames=fieldnames, dialect=self.dialect )
        writer.writeheader()
        x = [row for row in rows]
        for row in x:
            writer.writerow(row.item)


    def get_new_filename(self):
        return "results.shp"


class ShapeRow(object):
    def __init__(self, wrapped, fieldnames):
        self._wrapped = wrapped
        self.fieldnames = fieldnames
        
        self.item = self.get_item()
        self.new_fieldnames = []
    
    def get_item(self):
        out = {}
        for i,k in enumerate(self.fieldnames):
            out[k] = self._wrapped[i]
        return out

    def __getitem__(self, name):
        return self.item[name]

    def update(self, data):

        self.item.update(data)
        return self.item


    


class ShapeResource(object):
    def __init__(self, data):
        print "into shape resource"
        self.path = data['shapefile']
        self.source_shape = shapefile.Reader(self.path)
        self.get_fieldnames()
        

    def get_fieldnames(self):
        source_fields  = list(self.source_shape.fields)
        self.fieldnames = [x[0] for x in source_fields[1:]]



    def get_reader(self):
        reader = self.source_shape.records()
        for row in reader:
            yield ShapeRow(row, self.fieldnames)
        


    def get_stream(self):
        stream = StringIO.StringIO()
        return stream





    def write_to_stream(self, rows, fieldnames, stream):
        target_shape = shapefile.Writer()
        target_shape.fields  = self.source_shape.fields

        source_fields  = list(self.source_shape.fields)
        my_fieldnames = [x[0] for x in source_fields]
        extra_fields = [x for x in fieldnames if x not in my_fieldnames]

        

        all_fields = my_fieldnames+extra_fields
        all_fields.remove("DeletionFlag")
        #remap for 10 chars limit
        
        fields_map = {}
        fields_too_long = {}
        for field in all_fields:
            if len(field) > 9:
                fields_too_long[field] = True
            else:
                fields_map[field] = field

        new_fields_too_long = {}
        renamed = 0
        for key, value in fields_too_long.iteritems():
            new_value = key[:8]
            if new_value in fields_map.values():
                new_value += str(renamed)
                renamed += 1
            fields_map[key] = new_value



        #creating extra fields
        for f in extra_fields:
            new_field = (str(fields_map[f]),)
            target_shape.field(*new_field)        


        #scanning rows
        for row in rows:
            it = row.item
            record  =[]
            for i, x in enumerate(all_fields):
                try:
                    lkp = fields_map[x]
                    record.append(str(it[lkp]))
                except:
                    record.append(" ")
          
                
            target_shape.records.append(record)

        target_shape._shapes.extend(self.source_shape.shapes())

        #get temp dir.
        folder = tempfile.mkdtemp()
        #save shape
        #zip dir into zipfile
        #read zipfile and put it to stream
        out_file = os.path.join(folder, "result.shp")
        target_shape.save(out_file)
        
        folder2 = tempfile.mkdtemp()
        out_file_z = os.path.join(folder2, "shape.zip")
        zip_file(folder, out_file_z)

        stream.write(open(out_file_z).read())




    def get_new_filename(self):
        return "results.zip"

