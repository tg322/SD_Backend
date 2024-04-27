def get_user_by_email(email):
    from db_models import users
    from build_response import internal_response

    user = users.query.filter_by(Email=email).first()
    if user:
        user_details = {
            'id': user.id,
            'Email': user.Email,
            'PassHash': user.PassHash,
            'Role': user.Role
        }
        return internal_response(data=user_details, success=True)
    else:
        return internal_response(success=False, message='Failed to fetch user. From: get_user_by_email()')