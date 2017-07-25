import os
import re
import pprint
import xml.etree.ElementTree as ET

DATASET = "san-jose_california.osm"
PATH = "./"
OSMFILE = PATH + DATASET


def unique_user_id(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'uid' in element.attrib.keys():
            if element.attrib['uid'] not in users:
                users.add(element.attrib['uid'])
    return users


def max_length_user_id(users):
    length = 0
    for user_id in users:
        if len(user_id) > length:
            length = len(user_id)
    return length


def structure_user_id(users):
    """
    structure user id from unstructured format.
    :param users:
    :return:
    eg : 1      to 0000001
         2342   to 0002342
         31562  to 0031562
    """
    user_dict = set()
    for user_id in users:
        while len(user_id) < max_length_user_id(users):
            user_id = str('0' + user_id)
        user_dict.add(user_id)
    return user_dict


def unstructure_user_id(users):
    """
    restore the structured user id to unstructured.
    :param users:
    :return:
    eg : 1      to 0000001
         2342   to 0002342
         31562  to 0031562
    """
    user_dict = set()
    for user_id in structured:
        while user_id[0] is '0':
            user_id = user_id[1:]
        user_dict.add(user_id)
    return user_dict


def test():
    users = unique_user_id(OSMFILE)
    # structured = structure_user_id(users)
    # pprint.pprint(structured)
    max_length = max_length_user_id(users)
    print('Number of users: ', len(users))
    print('User ID maximum length', max_length)

    print_limit = 10
    for user_id in users:
        if len(user_id) < max_length:
            structured_id = user_id
            while len(structured_id) < max_length:
                structured_id = str('0' + structured_id)

            if print_limit > 0:
                print_limit -= 1
                print(user_id, "=>", structured_id)
            else:
                break


if __name__ == '__main__':
    test()
