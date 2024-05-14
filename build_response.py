from flask import jsonify

def internal_response(data=None, success=True, message=None):
    """
    Generates an internal response dictionary.
    Args:
        data (any, optional): The payload to include in the response. Defaults to None.
        success (bool): Indicates if the operation was successful.
        message (str, optional): Optional message describing the response.

    Returns:
        dict: A dictionary containing the response data.
    """
    response = {
        'success': success,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return response


def external_response(data=None, status=200, message=None):
    """
    Generates an external JSON response for API clients.
    Args:
        data (any, optional): The payload to include in the response. Defaults to None.
        status (int): HTTP status code to return.
        message (str, optional): Optional message describing the response.

    Returns:
        Response: A Flask response object with JSON data.
    """
    response = {
        'success': True if status >= 200 and status < 300 else False,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status
