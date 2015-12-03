import csv
import chardet
import unicodecsv




def test_read(filename):

    csv_rows = []
    stream = open(filename)
    dialect_csv = csv.Sniffer().sniff(stream.read())
    stream.seek(0)
    reader_csv = csv.DictReader(stream, dialect=dialect_csv)
    for row in reader_csv:
        print row




if __name__ == '__main__':
    test_read('d.csv')
    test_read('q.csv')

