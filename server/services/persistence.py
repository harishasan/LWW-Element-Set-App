"""
persistence layer for the operations on the set. A simple file is used instead of database because (1) database would
be overkill for type of operations being performed. Even for the case of 1 million concurrent monkey, file based
approach would be easily scalable because of append only (log like) implementation. Database would make
sense in case of other discussed scenario i.e. 100K documents and 1-10 monkeys collaborating. Detailed
 design of that scenario is discussed in read me.
"""
import os

FILE_PATH = os.environ['PERSISTENCE_PATH']
if not os.path.isfile(FILE_PATH):
    open(FILE_PATH, 'a').close()


def record(line):
    """
    appends the line on file
    :param line: line to append
    :return:
    """
    with open(FILE_PATH, 'a') as persistence_file:
        persistence_file.write(line)


def get_file_content(offset=0):
    """
    get file content as list of lines where each line represents on operation.

    # todo: enable gzip on server so all the data is sent in zipped format

    # the reason of sending raw text is the overall logic through which
    # client can sync without losing any data which is coming in from
    # other clients, during the file content is being transferred to that client.

    # todo: find a better way to send updates, currently server has to
    # read complete file, which is a lot of io, rather server should cache the writes,
    # and dump the earliest records once size of cache reaches a certain limit.
    # there can be many other approaches as well e.g. files with rounding/rollover times

    :param offset: default 0, operation offset to send data from and onwards
    :return:
    """
    content = None

    with open(FILE_PATH) as f:
        if offset == 0:
            content = f.readlines()
        else:
            content = []
            for i, line in enumerate(f):
                if i >= offset:
                    content.append(line)

    return content
