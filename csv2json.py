#!env python
# -*- coding: utf-8 -*-

'''
Parse data from csv database and output json for the front-end.
'''

import argparse
import csv
import json
import sys
import locale
import string

def urlify(url):
    if not url.startswith('http'):
        return 'http://%s' % url
    return url

def moneyfy(amount):
    return locale.currency(amount, grouping=True).split('.')[0]

def parse_csv(file_path):
    '''Parse file '''

    locations = dict()

    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        reader.next()
        for i, row in enumerate(reader):
            if row[7] is 'Y':
                if row[0].endswith('...'):
                    print >> sys.stderr, "Line %i: %s" % (i, row[0])
                try:
                    locations[string.capwords(row[0])] = dict(
                        t=string.capwords(row[0]), #venue title
                        p=row[2].strip(), #lat,lng
                        i=row[3].strip(), #address
                        f=moneyfy(int(row[1] or 0)), #funding
                        s=urlify(row[4].strip()), #source
                        d=row[5].strip(), #description
                    )
                except ValueError, e:
                    print >> sys.stderr, "Error parsing row %i: %s" % (i, e)

    print json.dumps(locations, separators=(',', ':'))

def main():
    '''main'''
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', help='CSV file path')
    args = parser.parse_args()

    locale.setlocale(locale.LC_ALL, locale='en_GB')

    parse_csv(args.csv_path)

if __name__ == '__main__':
    main()
