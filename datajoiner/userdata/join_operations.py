import mimetypes 
import csv

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
        if lookup_value in lookup_dict:
            row.update(lookup_dict[lookup_value])
        out_rows.append(row)

    print out_rows



def get_iterable_resource(path):
    mime = mimetypes.guess_type(path)
    mime = mime[0]
    if mime == "text/csv":
        return CsvResource(path)



def get_csv_reader(path):
    stream = open(path)
    dialect = csv.Sniffer().sniff(stream.read(1024))
    stream.seek(0)
    reader = csv.DictReader(stream, dialect=dialect)
        
    return reader


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


class CsvResource(object):
    def __init__(self, path):
        self.path = path


    def get_csv_reader(self):
        stream = open(self.path)
        dialect = csv.Sniffer().sniff(stream.read(1024))
        stream.seek(0)
        reader = csv.DictReader(stream, dialect=dialect)
        return reader    

    def get_rows_iterable(self):
        reader = self.get_csv_reader()
        for row in reader:
            yield CsvRow(row)



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

