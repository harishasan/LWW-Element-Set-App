import json

from flask import Blueprint
from flask import request
from server.services import lww_element
from server.services import persistence

ELEMENT_SET_API_CONTROLLER = Blueprint('element_set_api_controller', __name__)

ERROR_INVALID_JSON_DATA = 'Add and Remove operations requires data in JSON format. Sample: ' \
    '{timestamp: unix_timestamp, value: value}'
ERROR_INVALID_BULK_OPERATION_DATA = 'Bulk operations API expects a list of Add/Remove operations. Sample: ' \
    '[{operation: add, data: {timestamp: timestamp, value: value}}]'


def verify_single_data_point(request):
    """
    verify data point sent from client
    :param request: client request object
    :return: error string, Data where data is map<key, value>
    """
    if not request.data:
        return json.dumps({'error': ERROR_INVALID_JSON_DATA}), None

    data = json.loads(request.data)
    if 'timestamp' not in data or 'value' not in data:
        return json.dumps({'error': ERROR_INVALID_JSON_DATA}), None

    return None, data


@ELEMENT_SET_API_CONTROLLER.route('/element-set/add', methods=['POST'])
def add():
    """
    REST API to add element into the set. Expect data in format {timestamp: unix_timestamp, value: value}
    # todo add exception handing in case data is malformed
    """
    error, data = verify_single_data_point(request)
    if error:
        return error, 400

    lww_element.add(data['value'], int(data['timestamp']))
    return json.dumps({})


@ELEMENT_SET_API_CONTROLLER.route('/element-set/remove', methods=['DELETE'])
def remove():
    """
    REST API to delete element from set. Expect data in format {timestamp: unix_timestamp, value: value}
    # todo add exception handing in case data is malformed
    """
    error, data = verify_single_data_point(request)
    if error:
        return error[0], error[1]

    lww_element.remove(data['value'], int(data['timestamp']))
    return json.dumps({})


@ELEMENT_SET_API_CONTROLLER.route('/element-set/contains', methods=['GET'])
def contains():
    """
    REST API to check if an element exists in the set
    """
    value = request.values.get('value')
    if value is None:
        return json.dump({'error': 'Provide the value in query parameter. Sample /element-set/contains?value=xxx'}), 400

    return json.dumps({'contains': lww_element.contains(value)})


@ELEMENT_SET_API_CONTROLLER.route('/element-set/bulk-operations', methods=['POST'])
def bulk_operations():
    """
    REST API to perform bulk inserts/remove operations. Expects data in format
    [{operation: add, data: {timestamp: timestamp, value: value}}]
    # todo add exception handing in case data is malformed
    """
    if not request.data:
        return json.dumps({'error': ERROR_INVALID_BULK_OPERATION_DATA}), 400

    operations = json.loads(request.data)
    if type(operations) is not list:
        return json.dumps({'error': ERROR_INVALID_BULK_OPERATION_DATA}), 400

    for item in operations:
        print item
        if 'timestamp' not in item['data'] or 'value' not in item['data']:
            return json.dumps(ERROR_INVALID_BULK_OPERATION_DATA), 400

        data = json.loads(item['data'])
        if item['operation'] == 'add':
            lww_element.add(data['value'], data['timestamp'])
        else:
            lww_element.remove(data['value'], data['timestamp'])

    return json.dumps({})


@ELEMENT_SET_API_CONTROLLER.route('/element-set/fetch-all-data', methods=['GET'])
def get_all_data():
    """
    REST API to fetch previous add/remove operations from server.
    Pass query parameter 'offset' if not all data is required, server will send data
    starting from passed operation offset.
    """
    if 'offset' in request.args:
        return json.dumps(persistence.get_file_content(int(request.args['offset'])))

    return json.dumps(persistence.get_file_content())
