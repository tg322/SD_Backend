# export interface IUserDetailsProps{
#     firstName:string;
#     lastName:string;
#     picture?:Blob;
#     email:string;
# }

# export interface ILoginDetailsProps{
#     permissionLevel:string;
#     authToken:string;
#     user:IUserDetailsProps;
# }



def login_user():

    """
        Login User Endpoint.

        purpose:
            To log a user in with provided details.

        Returns:
            dict: an external_response object.
    """

    from flask import request, jsonify, make_response
    from build_response import external_response
    from db_access_functions import get_user_by_email
    data = request.get_json()
    get_user_by_email_response = get_user_by_email(data['email'])

    if get_user_by_email_response['success']:
        user_data = get_user_by_email_response['data']
        from authentication_functions import check_password
        check_password_response = check_password(data['password'], user_data['passHash'])
        if check_password_response['success']:
            from authentication_functions import create_token
            token_response = create_token(user_data)

            if token_response['success']:
                # Initialize user dictionary correctly before using it

                user = {
                    'firstName': user_data['firstName'],
                    'lastName': user_data['lastName'],
                    'picture': '', #Picture not implemented yet
                    'email': user_data['email']
                }

                data = {
                    'permissionLevel': user_data['role'],
                    # 'token': token_response['data'],  # Ensure this passes the token, not the whole response
                    'user': user
                }
                
                # Define cookies to set
                cookies = [{
                    'key': 'token',
                    'value': token_response['data'],
                    'httponly': True,
                    'secure': False,   # Set to True in production
                    'samesite': 'Lax',
                    'max_age': 24 * 60 * 60
                }]

                response = external_response(
                    data = data,
                    status= 200,
                    message= 'Login Successful.',
                    success= True,
                    cookies= cookies
                                             
                )

            return response
        else:
            return external_response(status=400, message=check_password_response['message'])
    else:
        return external_response(status=400, message=get_user_by_email_response['message'])
    

def sign_up_user():

    """
        Sign Up User Endpoint.

        purpose:
            To create a new user, with provided details.

        Returns:
            dict: an external_response object.
    """

    from flask import request
    from build_response import external_response
    from db_access_functions import get_user_by_email, insert_user

    data = request.get_json()
    get_user_by_email_response = get_user_by_email(data['email'])

    #If fetching user was unsuccessful, return error from response
    if not get_user_by_email_response['success']:
        return external_response(status=400, message=get_user_by_email_response['message'])
    
    #If no user was found, continue with account creation
    if not get_user_by_email_response['data']:

        password = data['password'].encode('utf-8')
        from bcrypt import hashpw, gensalt
        hash = hashpw(password, gensalt())
        insert_user_response = insert_user(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], pass_hash=hash, role=1)

        if(insert_user_response['success']):
            user_data = insert_user_response
            from authentication_functions import create_token
            token_response = create_token(insert_user_response)

            if not token_response['success']:
                return external_response(status=400, message=token_response['message'])
            
            user = {
            'firstName': user_data['firstName'],
            'lastName': user_data['lastName'],
            'picture': '', #Picture not implemented yet
            'email': user_data['email']
            }

            response = {
                'permissionLevel': user_data['role'],
                'token': token_response['data'],  # Ensure this passes the token, not the whole response
                'user': user
            }
        
            return external_response(status=200, message='Account created successfully.', data=response)
        else:
            external_response(status=400, message=insert_user_response['message'])
    else:
        return external_response(status=404, message='Account already exists.')
    
    

    
    
