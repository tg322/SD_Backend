from flask import jsonify

def internal_response(data, success=True, message=None):
    """
    Generates an internal response dictionary.
    Args:
        data (any): The payload to include in the response.
        success (bool): Indicates if the operation was successful.
        message (str): Optional message describing the response.

    Returns:
        dict: A dictionary containing the response data.
    """
    return {
        'success': success,
        'message': message,
        'data': data
    }

def external_response(data, status=200, message=None):
    """
    Generates an external JSON response for API clients.
    Args:
        data (any): The payload to include in the response.
        status (int): HTTP status code to return.
        message (str): Optional message describing the response.

    Returns:
        Response: A Flask response object with JSON data.
    """
    response = {
        'success': True if status >= 200 and status < 300 else False,
        'message': message,
        'data': data
    }
    return jsonify(response), status
