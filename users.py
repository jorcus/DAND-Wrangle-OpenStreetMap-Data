import os
import re
import pprint
import xml.etree.ElementTree as ET

DATASET = "san-jose_california.osm"
PATH = "./"
OSMFILE = PATH + DATASET

def unique_user_ID(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'uid' in element.attrib.keys():
            if element.attrib['uid'] not in users:
                users.add(element.attrib['uid'])
    return users

def test():
    users = unique_user_ID(OSMFILE)
    print('Number of users: ', len(users))
    pprint.pprint(users)


if __name__ == '__main__':
    test()
