import mimetypes 
import csv
import tempfile
import StringIO
from django.core.files import File 
from .models import UserFile
from django.core.files.storage import default_storage

#VERY BRUTAL FOR NOW!
#SHOULD BE DONE BY A TASK RUNNER




def join_files(left_hand, right_hand, left_hand_field, right_hand_field=None):
    if not right_hand_field:
        right_hand_field = left_hand_field

    print "--uuu joining uuu--"
    print left_hand, right_hand, left_hand_field, right_hand_field

    resource_left = get_iterable_resource(left_hand.data_file.path )
    resource_right = get_iterable_resource(right_hand.data_file.path)



    #read all rows in the right ad put them in a dict, key is right_hand_field
    lookup_dict = {}
    for row in resource_right.get_rows_iterable():
        lookup_dict[row[right_hand_field]] = row.item


    out_rows = []    
    #scan all rows in the left and lookup on the dict, based on left_hand field
    for row in resource_left.get_rows_iterable():
        lookup_value = row[left_hand_field]
        joint_row = {}
        for fieldname in resource_right.fieldnames:
            joint_row[fieldname] = ''

        if lookup_value in lookup_dict:
            joint_row.update(lookup_dict[lookup_value])
            if left_hand_field == right_hand_field and right_hand_field in joint_row:
                del joint_row[right_hand_field]
            row.update(joint_row)
            row.decode()
        out_rows.append(row)

    #print out_rows

    fieldnames = resource_left.fieldnames + resource_right.fieldnames
    fieldnames.remove(right_hand_field)
    
    stream = StringIO.StringIO()
    dialect=resource_left.dialect
    print "*" *10
    print resource_left.dialect.escapechar
    print resource_right.dialect.escapechar
    print "*" *10

    writer = csv.DictWriter(stream, fieldnames=fieldnames,dialect=dialect )
    writer.writeheader()
    x = [row.item for row in out_rows]
    for row in x:
        print row
        writer.writerow(row)

    #print stream.getvalue()


    path = default_storage.get_available_name("result.csv")

    out_file = UserFile(user=left_hand.user)
    out_file.data_file.save(
        path,
        File(stream)
    )
    out_file.save()

    return out_file.data_file.path




def get_iterable_resource(path):
    mime = mimetypes.guess_type(path)
    mime = mime[0]
    if mime == "text/csv":
        return CsvResource(path)

 

class CsvRow(object):
    def __init__(self, wrapped):
        self._wrapped = wrapped
    @property
    def item(self):
        return self._wrapped

    def __getitem__(self, name):
        return self._wrapped[name]

    def update(self, data):
        return self.item.update(data)

    def decode(self):
        for x in self._wrapped:
            self._wrapped[x] =unicode(self._wrapped[x])


class CsvResource(object):
    def __init__(self, path):
        self.path = path
        self.fieldnames = []
        self.dialect = None


    def get_csv_reader(self):
        stream = open(self.path)
        dialect = csv.Sniffer().sniff(stream.read())
        stream.seek(0)
        reader = csv.DictReader(stream, dialect=dialect)
        self.fieldnames = reader.fieldnames
        self.dialect = dialect
        return reader    

    def get_rows_iterable(self):
        reader = self.get_csv_reader()
        for row in reader:
            yield CsvRow(row)


    def rewrite_as_stream(self, rows):
        pass



class ShapeRow(object):
    def __init__(self, wrapped):
        self._wrapped = wrapped
    @property
    def item(self):
        return self._wrapped

    def __getitem__(self, name):
        return self._wrapped[name]

    def update(self, data):
        return self.item.update(data)


class ShapeResource(object):
    def __init__(self, path):
        self.path = path


    def get_reader(self):
        stream = open(self.path)
        reader = None
        return reader    

    def get_rows_iterable(self):
        reader = self.reader()
        for row in reader:
            yield ShapeRow(row)

