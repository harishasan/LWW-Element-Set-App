"""
This python module implements LWW-Element-Set as described in wikipedia link below.
https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#LWW-Element-Set_(Last-Write-Wins-Element-Set)
"""


class LWWElementSet(object):
    """ implementation of LWW-Element-Set
    """

    # added values, map<value, timestamp>
    __add_set = None
    # removed values, map<value, timestamp>
    __remove_set = None
    __bias = None

    def __init__(self, bias='add'):
        self.__add_set = {}
        self.__remove_set = {}
        if bias != 'add' and bias != 'remove':
            bias = 'add'

        self.__bias = bias

    def contains(self, value):
        """
        Checks if an element exists in the set using a combination of add set,
        remove set and bias values

        Arguments:
            value {string} -- [value to be added in the set]

        Returns:
            [boolean] -- [True if element exists, False otherwise]
        """

        if value not in self.__add_set:
            return False

        if value not in self.__remove_set:
            return True

        if self.__add_set[value] == self.__remove_set[value]:
            return self.__bias == 'add'

        return self.__add_set[value] > self.__remove_set[value]

    def add(self, value, timestamp):
        """add element into the set with given timestamp

        Arguments:
            value {string} -- value to be added
            timestamp {integer} -- unix timestamp denoting the operation time
        """

        self.__add_set[value] = timestamp
        # print '----------------- add set -----------------'
        # print self.__add_set

    def remove(self, value, timestamp):
        """removes element from set at given timestamp

        Arguments:
            value {string} -- value to remove
            timestamp {integer} -- unix timestamp denoting the operation time
        """

        self.__remove_set[value] = timestamp
        # print '----------------- remove set --------------'
        # print self.__remove_set

    def merge(self, lww_element_set):
        """merges the given set with current set.
        For merging within a (add/remove) set, preference is given to latest timestamp

        Arguments:
            lww_element_set {LWWElementSet} -- set to merge with current set

        Returns:
            [LWWElementSet] -- reference to current set
        """

        self.__merge_sets(self.__add_set, lww_element_set.__add_set)
        self.__merge_sets(self.__remove_set, lww_element_set.__remove_set)
        return self

    def __merge_sets(self, first, second):
        for key in second:
            if key not in first:
                first[key] = second[key]
            else:
                if second[key] > first[key]:
                    first[key] = second[key]
