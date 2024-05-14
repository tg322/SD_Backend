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

    from flask import request
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
                    'picture': '',
                    'email': user_data['email']
                }

                response = {
                    'permissionLevel': user_data['role'],
                    'token': token_response['data'],  # Ensure this passes the token, not the whole response
                    'user': user
                }

            return external_response(data=response, status=200, message='Login Successful.')
        else:
            return external_response(status=400, message=check_password_response['message'])
    else:
        return external_response(status=400, message=get_user_by_email_response['message'])