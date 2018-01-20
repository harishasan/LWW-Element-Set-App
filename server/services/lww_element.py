"""
this module perform the operations add/remove/contain operations on element set.
"""
from server.services import persistence
from core.LWWElementSet import LWWElementSet

LWW_ELEMENT_SET = LWWElementSet()


def add(value, timestamp):
    """
    adds element into the set and also persists the operation in the log file
    :param value: value to persist
    :param timestamp: operation unix timestamp
    :return:
    """
    LWW_ELEMENT_SET.add(value, timestamp)
    persistence.record('{},{},{}\n'.format('add', value, timestamp))
    print 'SERVER APP: a new element as has been pushed in the LWW-Element-Set'

def remove(value, timestamp):
    """
    removes element from the set and also persists the operation in the log file
    :param value: value to remove
    :param timestamp: operation unix timestamp
    :return:
    """
    LWW_ELEMENT_SET.remove(value, timestamp)
    persistence.record('{},{},{}\n'.format('remove', value, timestamp))
    print 'SERVER APP: an element as has been removed from the LWW-Element-Set'


def contains(value):
    """
    checks if element exists in the set
    :param value: value to check
    :return: True if element exists, False otherwise
    """
    return LWW_ELEMENT_SET.contains(value)
