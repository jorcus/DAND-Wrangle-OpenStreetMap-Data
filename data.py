import codecs
import json
from pymongo import MongoClient
import xml.etree.ElementTree as ET
from tags import problemchars
from audit import update_name, mapping

DATASET = "san-jose_california.osm"
PATH = "./"
OSMFILE = PATH + DATASET

def shape_element(element):
    if element.tag == "node" or element.tag == "way":
        node = {
            "id": element.attrib['id'],
            "type": element.tag,
            "visible": element.get("visible"),
            "created": {
                "version": element.get("version"),
                "changeset": element.get("changeset"),
                "timestamp": element.get("timestamp"),
                "user": element.get("user"),
                "uid": element.get("uid")
            }
        }

        if element.find("tag") is not None:
            node["address"] = {}
            for tag in element.iter("tag"):
                if tag.attrib['k'] == "addr:housenumber":
                    node["address"]["housenumber"] = tag.attrib['v']
                if tag.attrib['k'] == "addr:postcode":
                    node["address"]["postcode"] = tag.attrib['v']
                if tag.attrib['k'] == "addr:street":
                    node["address"]["street"] = tag.attrib['v']

        for nd_elem in element.iter("nd"):
            if 'node_refs' not in node:
                node['node_refs'] = []
            node['node_refs'].append(nd_elem.get("ref"))

        if element.get("lat") and element.get("lon"):
            node["pos"] = [float(element.get("lat")), float(element.get("lon"))]

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


if __name__ == '__main__':
    data = process_map(OSMFILE, True)
    print(data[0])