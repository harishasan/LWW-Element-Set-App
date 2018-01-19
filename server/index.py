if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import json
import os
from flask import Flask

from controllers.api.element_set_api_controller import ELEMENT_SET_API_CONTROLLER

APP = Flask(__name__)
APP.register_blueprint(ELEMENT_SET_API_CONTROLLER, url_prefix='/api')


def run_server():
    """
    starts the server
    """
    print('starting server...')
    APP.run(host='0.0.0.0', port=int(os.environ['PORT']), threaded=True)


@APP.errorhandler(404)
def page_not_found(ex):
    """
    Default handler for unhandled routes
    """
    content = json.dumps({'error': 'resource not found'})
    return content, 404

if __name__ == "__main__":
    run_server()
