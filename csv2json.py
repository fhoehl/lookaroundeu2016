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
from collections import namedtuple

from babel.numbers import format_currency

VENUE_TITLE = 0
VENUE_GEO = 3
VENUE_ADDRESS = 4
VENUE_FUNDING = 2
VENUE_FUNDING_CURRENCY = 1
VENUE_SOURCE = 5
VENUE_DESCRIPTION = 6
VENUE_PUBLISH = 8

Row = namedtuple('Row', [
    'title',
    'geo', 'address',
    'funding', 'currency',
    'source',
    'publish',
    'description'])

def urlify(url):
    '''Append http:// in front of url'''
    if not url.startswith('http'):
        return 'http://%s' % url
    return url

def moneyfy(currency, amount):
    '''Format amount of money according to a locale'''
    if currency.lower() in ('€', 'eur'):
        return format_currency(int(amount), 'EUR', locale='en_GB').split('.')[0]
    elif currency.lower() in ('£', 'gbp'):
        return format_currency(int(amount), 'GBP', locale='en_GB').split('.')[0]
    return amount

def maprow(line_number, row):
    '''Extract data from a row'''
    try:
        return Row(
            title=string.capwords(row[VENUE_TITLE]),
            geo=row[VENUE_GEO].strip(),
            address=row[VENUE_ADDRESS].strip(),
            funding=moneyfy(row[VENUE_FUNDING_CURRENCY], int(row[VENUE_FUNDING] or 0)),
            source=urlify(row[VENUE_SOURCE].strip()),
            description=row[VENUE_DESCRIPTION].strip(),
            currency=row[VENUE_FUNDING_CURRENCY],
            publish=True if row[VENUE_PUBLISH] is 'Y' else False)
    except ValueError, exception:
        print >> sys.stderr, "Error parsing row %i: %s" % (line_number, exception)
        return None

def parse_csv(file_path):
    '''Parse file'''

    locations = dict()

    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        reader.next()
        for line_number, row in enumerate(reader):
            venue = maprow(line_number, row)
            if venue and venue.publish:
                if venue.title.endswith('...'):
                    print >> sys.stderr, "Line %i: %s" % (line_number, row[0])

                locations[venue.title] = dict(
                    t=venue.title,
                    p=venue.geo,
                    i=venue.address,
                    f=venue.funding,
                    s=venue.source,
                    d=venue.description,)

        print json.dumps(locations, separators=(',', ':'))

def main():
    '''main'''
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', help='CSV file path')
    args = parser.parse_args()
    parse_csv(args.csv_path)

if __name__ == '__main__':
    main()
