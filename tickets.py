def get_tickets():
    from flask import request
    from build_response import external_response
    from authentication_functions import verify_token
    auth_token = request.cookies.get('token')
    from authentication_functions import decrypt_token
    decrypted_token = decrypt_token(auth_token)
    print(decrypted_token)
    verify_token_response = verify_token(decrypted_token['data'])
    if verify_token_response['success']:
        from db_access_functions import get_all_tickets
        response = get_all_tickets()
        if response['success']:
            return external_response(status=200, success=True, message='Tickets retrieved successfully.', data=response['data'])
        else:
            return external_response(
                        status= 403,
                        message= 'Failed to fetch tickets',
                        success= False                       
                    )
    else:
        return external_response(
                        status= 403,
                        message= 'Token valid',
                        success= False                       
                    )
        