"""
Offline-to-Online Sync - This Chaos Monkey mimics a user who adds and removes sets offline, and then goes online
expecting their sets to sync up.
"""
import os
import time
import random
import requests
from datetime import datetime
from calendar import timegm
import json


def start():
    """
    launches the offline-to-online monkey
    :return:
    """
    max_seconds = int(os.environ['OFFLINE_TO_ONLINE_MONKEY_MAX_DELAY_SECONDS'])

    while True:
        time_to_sleep = random.randint(0, max_seconds)
        server_address = os.environ['SERVER_ADDRESS']

        # holds tuple(operation_type, data)
        cached_requests = []
        previous_adds = [0]
        # at max I am caching 10 offline API calls
        for index in range(0, random.randint(0, 10)):
            random_value = random.randint(0, 10000)
            add = random_value % 2 == 0
            # if the api call is add, pick a value between 0 and ten thousand
            # if api call is remove, pick a number from previous adds
            value = random_value if add else previous_adds[random_value % len(previous_adds)]

            if add:
                # todo: this list might become very big eventually, do an alternate implementation
                previous_adds.append(value)

            data = {'value' : value, 'timestamp': timegm(datetime.utcnow().utctimetuple())}

            if add:
                cached_requests.append(('add', json.dumps(data)))
            else:
                cached_requests.append(('remove', json.dumps(data)))

        url = server_address + '/api/element-set/bulk-operations'
        operations = []
        for item in cached_requests:
            if item[0] == 'add':
                operations.append({'operation': 'add', 'data': item[1]})
            else:
                operations.append({'operation': 'remove', 'data': item[1]})

        # print json.dumps(operations)
        print 'posting data on server, {} operations'.format(len(operations))
        requests.post(url, data=json.dumps(operations))
        print 'done, going to sleep for {} second(s)'.format(time_to_sleep)
        time.sleep(time_to_sleep)

if __name__ == "__main__":
    start()

