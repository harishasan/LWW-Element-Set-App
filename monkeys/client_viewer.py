"""
This Chaos Monkey adds and remove sets at random intervals.
"""

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import random
from calendar import timegm
from datetime import datetime
import os
import requests
import json
import time

from core.LWWElementSet import LWWElementSet


def build_random_set():
    """
    builds a random initial set with elements between 0-25.
    :return: newly created set
    """
    lww_element_set = LWWElementSet()
    for index in range(0, random.randint(0, 25)):
        if index % 2 == 0:
            lww_element_set.add(random.randint(0, 25), timegm(datetime.utcnow().utctimetuple()))
        else:
            lww_element_set.remove(random.randint(0, 25), timegm(datetime.utcnow().utctimetuple()))

    return lww_element_set


def build_lww_element_set_from_data(data):
    """
    TODO: ensure data is sent from server in correct format
    :param data: raw data fetched from server
    :return: newly built set
    """
    element_set = LWWElementSet()
    for item in data:
        splits = item.split(',')
        timestamp = int(splits[2])
        value = splits[1]

        if splits[0] == 'add':
            element_set.add(value, timestamp)
        else:
            element_set.remove(value, timestamp)

    return element_set


def get_and_merge_new_records(url, lww_element_set):
    """
    gets the latest data from server and merges it in passed element set
    :param url: url to fetch data from
    :param lww_element_set: set to update
    :return: size of fetched data
    """
    response = requests.get(url)
    data = json.loads(response.text)
    new_set = build_lww_element_set_from_data(data)
    lww_element_set = lww_element_set.merge(new_set)
    return len(data)


def fetch_all_data(url):
    """
    fetches all data from server, used for first time fetch
    :param url: url to fetch data
    :return: fetched data as python list
    """
    result = requests.get(url)
    return json.loads(result.text)


def start():
    """
    launches client viewer monkey and runs indefinitely.
    :return:
    """
    print '----------------------------'
    print 'CLIENT VIEWER is starting'
    print '----------------------------'
    lww_element_set = build_random_set()
    print 'built a random local set'
    # perform the first time fetching
    # print '-----------original '
    # print lww_element_set
    server_address = os.environ['SERVER_ADDRESS']
    fetch_data_url = server_address + '/api/element-set/fetch-all-data'
    all_data = fetch_all_data(fetch_data_url)
    print 'fetch all data from server'
    server_element_set = build_lww_element_set_from_data(all_data)
    print 'merged the local and server data'
    lww_element_set = lww_element_set.merge(server_element_set)
    fetched_record_count = len(all_data)
    #print fetched_record_count
    #print '-----------updated'
    #print lww_element_set

    # near real time fetching via pooling after every 2 seconds
    # in order to make it more interactive, use web sockets
    while True:
        print '--------------------------------------------------------'
        print 'CLIENT VIEWER: fetching new data from server'
        print '--------------------------------------------------------'
        connect_url = '{}?offset={}'.format(fetch_data_url, fetched_record_count)
        print connect_url
        fetched_record_count += get_and_merge_new_records(connect_url, lww_element_set)
        time.sleep(2)

if __name__ == "__main__":
    start()