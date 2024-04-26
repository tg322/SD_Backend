

def get_key():

    from db_models import encryption_key
    key_data = encryption_key.query.first()
    if key_data:
        print(key_data)
        return key_data.encrypt_key
    else:
        return None 