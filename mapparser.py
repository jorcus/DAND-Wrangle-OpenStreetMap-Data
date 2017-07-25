import os
import re
import pprint
import xml.etree.ElementTree as ET

DATASET = "san-jose_california.osm"
PATH = "./"
OSMFILE = PATH + DATASET


def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag not in tags:
            tags[elem.tag] = 1
        else:
            tags[elem.tag] += 1
    return tags


def count_tags_total(tags):
    num_tags = 0
    for key, value in tags.items(): num_tags += value
    return num_tags


def test():
    tags = count_tags(OSMFILE)
    pprint.pprint(tags)

    print('Numbers of tag: ', len(tags))
    print('Numbers of tag elements: ', count_tags_total(tags))


if __name__ == '__main__':
    test()
