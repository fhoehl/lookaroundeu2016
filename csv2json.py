#!env python
# -*- coding: utf-8 -*-

'''
Parse data from csv database and output json for the front-end.
'''

import argparse
import csv
import json

def parse_csv(file_path):
    '''Parse file '''

    locations = dict()

    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        reader.next()
        for row in reader:
            locations[row[0]] = dict(
                t=row[0], #venue title
                p=row[2].strip(), #lat,lng
                i=row[1].strip(), #address
                f=int(row[3].replace('£', '').replace(',', '') or 0), #funding
                s=row[4].strip(), #source
                d=row[5].strip(), #description
            )

    print json.dumps(locations, separators=(',', ':'))

def main():
    '''main'''
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', help='CSV file path')
    args = parser.parse_args()

    parse_csv(args.csv_path)

if __name__ == '__main__':
    main()
