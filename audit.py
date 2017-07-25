import os
import re
import pprint
import xml.etree.ElementTree as ET
from collections import defaultdict

DATASET = "san-jose_california.osm"
PATH = "./"
OSMFILE = PATH + DATASET

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = {"St": "Street",
           "St.": "Street",
           "Ave": "Avenue",
           "Ave.": "Avenue",
           "Rd": "Road",
           "Rd.": "Road",
           "Blvd": "Boulevard",
           "Blvd.": "Boulevard",
           "Cir": "Circle",
           "Cir.": "Circle",
           "Ct": "Court",
           "Ct.": "Court",
           "Dr": "Drive",
           "Dr.": "Drive",
           "Pl": "Place",
           "Pl.": "Place",
           "Pkwy": "Parkway",
           "Pkwy.": "Parkway",
           "Hwy": "Highway",
           "Hwy.": "Highway",
           "Sq": "Square",
           "Sq.": "Square",
           }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    m = street_type_re.search(name)
    if m.group() not in expected:
        if m.group() in mapping.keys():
            name = re.sub(m.group(), mapping[m.group()], name)
    return name


def test():
    st_types = audit(OSMFILE)
    # pprint.pprint(dict(st_types)) #print out dictonary of potentially incorrect street types
    print_limit = 10
    for st_type, ways in st_types.items(): # .iteritems() for python2
        for name in ways:
            if street_type_re.search(name).group() in mapping:
                better_name = update_name(name, mapping)
                if print_limit > 0:
                    print_limit -= 1
                    print (name, "=>", better_name)
                else:
                    break


if __name__ == '__main__':
    test()


def test():
    users = unique_user_ID(OSMFILE)
    print('Number of users: ', len(users))
    pprint.pprint(users)


if __name__ == '__main__':
    test()
