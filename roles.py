def get_roles():
    from flask import request
    from build_response import external_response
    from authentication_functions import verify_token
    auth_token = request.cookies.get('token')
    if auth_token:
        from authentication_functions import decrypt_token
        decrypted_token = decrypt_token(auth_token)
        decrypted_token_data = decrypted_token['data']
        verify_token_response = verify_token(decrypted_token_data)
        if decrypted_token_data['permissionLevel'] >= 1:
            if verify_token_response['success']:
                from db_access_functions import get_all_roles
                get_roles_response = get_all_roles()
                if get_roles_response['success']:
                    return external_response(
                    status=200,
                    message='Roles retrieved successfully.',
                    data=get_roles_response['data'],
                    success=True
                    )
                else:
                    return external_response(
                    status=200,
                    message='Roles retrieved successfully.',
                    data=get_roles_response['data'],
                    success=True
                    )
            else:
                # return token invalid
                return external_response(
                    status=403,
                    message='Token invalid.',
                    success=False
                    )
        else:
            # return permission not high enough
            return external_response(
                status=403,
                message='Permission level not high enough.',
                success=False
                )
    else:
        # return no token present
        return external_response(
            status=403,
            message='No token present.',
            success=False
            )