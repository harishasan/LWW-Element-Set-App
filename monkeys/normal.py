"""
Normal - This Chaos Monkey adds and remove sets at random intervals.
"""
import os
import time
import random
import requests
from datetime import datetime
import json
from calendar import timegm


def start():
    """
    launches the normal monkey
    :return:
    """
    print '----------------------------'
    print 'NORMAL MONKEY is starting'
    print '----------------------------'
    previous_adds = [0]
    max_seconds = int(os.environ['NORMAL_MONKEY_MAX_DELAY_SECONDS'])

    while True:
        time_to_sleep = random.randint(0, max_seconds)
        server_address = os.environ['SERVER_ADDRESS']
        # perform add operation if random number is even, and remove operation otherwise
        add = time_to_sleep % 2 == 0
        url = '/api/element-set/add' if add else '/api/element-set/remove'
        # if the api call is add, pick a value between 0 and ten thousand
        # if api call is remove, pick a number from previous adds
        random_value = random.randint(0, 10000)
        value = random_value if add else previous_adds[random_value % len(previous_adds)]

        if add:
            # todo: this list might become very big eventually, implement an alternate approach
            previous_adds.append(value)

        data = {'value' : value, 'timestamp': timegm(datetime.utcnow().utctimetuple())}

        if add:
            print '--------------------------------------------------------'
            print 'NORMAL MONKEY sending an add request'
            print '--------------------------------------------------------'
            requests.post(server_address + url, data=json.dumps(data))
        else:
            print '--------------------------------------------------------'
            print 'NORMAL MONKEY sending a delete request'
            print '--------------------------------------------------------'
            requests.delete(server_address + url, data=json.dumps(data))

        print 'Normal Monkey is now going to sleep for {} second(s)'.format(time_to_sleep)
        time.sleep(time_to_sleep)

if __name__ == "__main__":
    start()

