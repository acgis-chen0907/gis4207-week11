import csv
import geom_obj03 as go

new_csv = r"..\..\..\..\data\week_11_output\stops.csv"

def test_geom_obj03():
    go.write_report(new_csv)
    with open (new_csv) as infile:
        next(infile)
        reader = csv.reader(infile)
        for row in reader:
            test_row = row
            break
    actual = test_row
    expected = ['CH080', '1708', '837', '27.751324120559666', '232']
    assert actual == expected