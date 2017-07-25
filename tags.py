import os
import re
import pprint
import xml.etree.ElementTree as ET

DATASET = "san-jose_california.osm"
PATH = "./"
OSMFILE = PATH + DATASET

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        key = element.attrib['k']
        if re.search(lower, key):
            keys['lower'] += 1
        elif re.search(lower_colon, key):
            keys['lower_colon'] += 1
        elif re.search(problemchars, key):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
    return keys


def process_map_tags(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys


def test():
    keys = process_map_tags(OSMFILE)
    pprint.pprint(keys)


if __name__ == '__main__':
    test()
