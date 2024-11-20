
def get_user_by_email(email):

    """
    Fetches user by provided email and returns the corresponding user information.
    
    Args:
        email (string, required): The email to be used to search the database for.

    Returns:
        dict: an internal_response object.
    """


    try:
        from db_models import users
        from build_response import internal_response

        user = users.query.filter_by(Email=email).first()
        
        if user:
            user_details = {
                'id': user.id,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.Email,
                'passHash': user.PassHash,
                'role': user.Role
            }
            return internal_response(data=user_details, success=True, message='User found successfully.')
        else:
            return internal_response(success=False, message='No user found with the provided email.')

    except Exception as e:
        return internal_response(success=False, message=f'An error occurred: {str(e)}')
    


def insert_user(first_name, last_name, email, pass_hash, role = 1):

    """
    Inserts a user into the database users table.

    Args:
        first_name (string, required): The users first name.
        last_name (string, required): The users last name.
        email (string, required): The users email address.
        pass_hash (string, required): The users password in hashed format (Not plain text).
        role (integer, optional): The users intended access role, defaults to 1 ('user') if not provided.

    Returns:
        dict: an internal_response object.
    """

    try:

        from db_models import users, db
        from build_response import internal_response

        new_user = users(first_name=first_name, last_name=last_name, Email=email, PassHash=pass_hash, Role=role)
        db.session.add(new_user)
        db.session.commit()

        user_details = {
            'id': new_user.id,
            'firstName': new_user.first_name,
            'lastName': new_user.last_name,
            'email': new_user.Email,
            'passHash': new_user.PassHash,
            'role': new_user.Role
        }

        return internal_response(success=True, message='User created successfully.', data=user_details)
    
    except Exception as e:
        return internal_response(success=False, message=f'An error occurred: {str(e)}')

def get_all_tickets():
    from db_models import Tickets, ticket_category, users, db
    from sqlalchemy.orm import aliased
    from build_response import internal_response
    category_alias = aliased(ticket_category)
    user_alias = aliased(users)

    all_tickets = []

    response = {}
    
    all_tickets = db.session.query(Tickets, category_alias, user_alias)\
    .join(category_alias, Tickets.ticket_category == category_alias.id)\
    .join(user_alias, Tickets.ticket_from_id == user_alias.id).all()
    
    if all_tickets:
        serialized_data = [
        {
            'ticket_id': ticket.id,
            'ticket_subject': ticket.ticket_subject,
            'category': category.category,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'ticket_date': ticket.ticket_date_sent,
            'ticket_status': ticket.ticket_status,
        }
        for ticket, category, user in all_tickets
        ]

        response = {'tickets': serialized_data}
        
        return internal_response(success=True, message='Tickets retrieved successfully.', data=response)
    else:
        return internal_response(success=False, message='Failed to fetch tickets')

    
