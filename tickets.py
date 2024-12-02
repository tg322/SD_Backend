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
                        message= 'Token invalid',
                        success= False                       
                    )
    
def get_ticket_by_id():
    from flask import request
    from build_response import external_response
    from authentication_functions import verify_token
    auth_token = request.cookies.get('token')
    from authentication_functions import decrypt_token
    decrypted_token = decrypt_token(auth_token)
    print(decrypted_token)
    verify_token_response = verify_token(decrypted_token['data'])

    if verify_token_response['success']:
        from db_access_functions import get_ticket
        data = request.get_json()
        response = get_ticket(data['id'])
        if response['success']:
            return external_response(status=200, success=True, message='Ticket retrieved successfully.', data=response['data'])
        else:
            return external_response(
                        status= 403,
                        message= 'Failed to fetch tickets',
                        success= False                       
                    )
    else:
        return external_response(
                        status= 403,
                        message= 'Token invalid',
                        success= False                       
                    )


def close_ticket():
    from flask import request
    from build_response import external_response
    from authentication_functions import verify_token
    auth_token = request.cookies.get('token')
    from authentication_functions import decrypt_token
    decrypted_token = decrypt_token(auth_token)
    print(decrypted_token)
    verify_token_response = verify_token(decrypted_token['data'])

    if verify_token_response['success']:
        from db_access_functions import closeTicketByID
        data = request.get_json()
        response = closeTicketByID(data['id'])
        if response['success']:
            return external_response(status=200, success=True, message='Ticket closed successfully.')
    else:
        return external_response(
                        status= 403,
                        message= 'Token invalid',
                        success= False                       
                    )

def open_ticket():
    from flask import request
    from build_response import external_response
    from authentication_functions import verify_token
    auth_token = request.cookies.get('token')
    from authentication_functions import decrypt_token
    decrypted_token = decrypt_token(auth_token)
    print(decrypted_token)
    verify_token_response = verify_token(decrypted_token['data'])

    if verify_token_response['success']:
        from db_access_functions import openTicketByID
        data = request.get_json()
        response = openTicketByID(data['id'])
        if response['success']:
            return external_response(status=200, success=True, message='Ticket opened successfully.')
    else:
        return external_response(
                        status= 403,
                        message= 'Token invalid',
                        success= False                       
                    )
    
def delete_ticket():
    from flask import request
    from build_response import external_response
    from authentication_functions import verify_token
    auth_token = request.cookies.get('token')
    from authentication_functions import decrypt_token
    decrypted_token = decrypt_token(auth_token)
    decrypted_token_data = decrypted_token['data']
    verify_token_response = verify_token(decrypted_token_data)
    if decrypted_token_data['permissionLevel'] >=2:
        if verify_token_response['success']:
            from db_access_functions import deleteTicketByID
            data = request.get_json()
            response = deleteTicketByID(data['id'])
            if response['success']:
                return external_response(status=200, success=True, message='Ticket deleted successfully.')
        else:
            return external_response(
                    status= 403,
                    message= 'Token invalid',
                    success= False                       
                    )
    else:
        return external_response(
                status= 403,
                message= 'Permission level too low.',
                success= False                       
                )

def create_ticket():
    from flask import request
    from build_response import external_response
    from authentication_functions import verify_token
    auth_token = request.cookies.get('token')
    data = request.get_json()
    from authentication_functions import decrypt_token
    decrypted_token = decrypt_token(auth_token)
    decrypt_token_data = decrypted_token['data']
    verify_token_response = verify_token(decrypt_token_data)

    if verify_token_response['success']:
        from db_access_functions import create_ticket
        response = create_ticket(data['ticketSubject'], data['ticketBody'], data['ticketCategory'], decrypt_token_data['user_id'])
        if response['success']:
            return external_response(
                    status= 200,
                    message= 'Ticket created successfully.',
                    success= True                       
                    )
        else:
            return external_response(
                    status= 403,
                    message= response['message'],
                    success= False                       
                    )
    else:
        return external_response(
                status= 403,
                message= 'Token invalid',
                success= False                       
                )
    
def get_ticket_categories():
    from flask import request
    from build_response import external_response
    from authentication_functions import verify_token
    auth_token = request.cookies.get('token')
    from authentication_functions import decrypt_token
    decrypted_token = decrypt_token(auth_token)
    decrypt_token_data = decrypted_token['data']
    verify_token_response = verify_token(decrypt_token_data)

    if verify_token_response['success']:
        from db_access_functions import get_all_categories
        response = get_all_categories()
        if response['success']:
            return external_response(
                    status= 200,
                    message= 'Categories retrieved successfully.',
                    success= True,
                    data=response['data']                       
                    )
        else:
            return external_response(
                    status= 403,
                    message= response['message'],
                    success= False                       
                    )
    else:
        return external_response(
                status= 403,
                message= 'Token invalid',
                success= False                       
                )