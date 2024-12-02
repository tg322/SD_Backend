
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


def get_ticket(id):
    from db_models import Tickets, ticket_category, users, db
    from sqlalchemy.orm import aliased
    from build_response import internal_response
    category_alias = aliased(ticket_category)
    user_alias = aliased(users)
    ticket = db.session.query(Tickets, category_alias, user_alias)\
                .join(category_alias, Tickets.ticket_category == category_alias.id)\
                .join(user_alias, Tickets.ticket_from_id == user_alias.id)\
                .filter(Tickets.id == id).first()
    if ticket:
        ticket, category, user = ticket

        serialized_data = {
            'ticket_id': ticket.id,
            'ticket_subject': ticket.ticket_subject,
            'ticket_body': ticket.ticket_body,
            'category': category.category,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'ticket_date': ticket.ticket_date_sent,
            'ticket_status': ticket.ticket_status,
        }

        return internal_response(success=True, message='Ticket retrieved successfully.', data=serialized_data)
    else:
        return internal_response(success=False, message='Failed to fetch ticket.')

def closeTicketByID(id):
    from db_models import Tickets, db
    from build_response import internal_response
    ticket = Tickets.query.get(id)
    ticket.ticket_status = 'Closed'
    db.session.commit()
    return internal_response(success=True, message='Ticket closed successfully.')

def openTicketByID(id):
    from db_models import Tickets, db
    from build_response import internal_response
    ticket = Tickets.query.get(id)
    ticket.ticket_status = 'Open'
    db.session.commit()
    return internal_response(success=True, message='Ticket opened successfully.')

def deleteTicketByID(id):
    from db_models import Tickets, db
    from build_response import internal_response
    Tickets.query.filter(Tickets.id == id).delete()
    db.session.commit()
    return internal_response(success=True, message='Ticket deleted successfully.')

def get_all_roles():
    from db_models import roles, db
    userRoles = roles.query.all()

    all_userRoles = []

    if userRoles:
        from build_response import internal_response
        for userRole in userRoles:
            all_userRoles.append({
                'id': userRole.id,
                'role': userRole.role_name
            })
        return internal_response(success=True, message='Roles retrieved successfully.', data=all_userRoles)
    else:
        return internal_response(success=False, message='Roles retrieved unsuccessfully.')
    

def create_ticket(ticket_subject, ticket_body, ticket_category, ticket_from_id):

    try:

        from db_models import Tickets, db
        from build_response import internal_response

        new_ticket = Tickets(
            ticket_subject=ticket_subject, 
            ticket_body=ticket_body, 
            ticket_category=ticket_category, 
            ticket_from_id=ticket_from_id
        )
        db.session.add(new_ticket)
        db.session.commit()

        return internal_response(success=True, message='Ticket created successfully.')
    
    except Exception as e:
        return internal_response(success=False, message=f'An error occurred: {str(e)}')
    
def get_all_categories():
    try:

        from db_models import ticket_category, db
        from build_response import internal_response

        categories = ticket_category.query.all()

        all_categories = []

        if categories:
            for category in categories:
                all_categories.append({
                    'id': category.id,
                    'category': category.category
                })

        return internal_response(success=True, message='Categories retrieved successfully.', data=all_categories)

    except Exception as e:
        return internal_response(success=False, message=f'An error occurred: {str(e)}')