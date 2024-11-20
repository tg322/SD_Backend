
def get_key():

    """
    Retrieves the secret key for encryption.

    Returns:
        encrypt_key dict for use when encrypting.
    """

    from build_response import internal_response

    from db_models import encryption_key
    key_data = encryption_key.query.first()
    if key_data:
        return internal_response(data=key_data.encrypt_key, success=True)
    else:
        return internal_response(success=False, message='Failed to fetch secret key from DB. From: get_key()')
      
def generate_encrypted_payload(payload):

    """
    Generates encrypted payload from specified data.

    Args:
        payload (any): The payload to encrypt.

    Returns:
        The data passed, encrypted in AES 256
    """ 

    from build_response import internal_response
    import json
    from jwcrypto import jwe, jwk

    payload_str = json.dumps(payload)
    key_str_response = get_key()

    if key_str_response['success'] == True:
        
        key = jwk.JWK.from_json(key_str_response['data'])

        jwetoken = jwe.JWE(plaintext=payload_str.encode('utf-8'),
                           protected={"alg": "A256KW", "enc": "A256CBC-HS512"})
        jwetoken.add_recipient(key)
        encrypted_payload = jwetoken.serialize(compact=True)

        return internal_response(data=encrypted_payload, success=True)
    else:
        return key_str_response
     
    
def check_password(plain_text_password, hashed_password):

    """
        Compares a hashed provided password against a stored or other password.

        Args:
            plain_text_password (string): The password to be hashed and checked.
            hashed_password (string | bytes): The stored or other hashed password to be checked against.

        Returns:
            True if the plain_text_password is the same as the existing provided hashed_password.
            else: False if the plain_text_password is not the same.
        """ 

    import bcrypt

    from build_response import internal_response

    plain_text_password_bytes = plain_text_password.encode('utf-8')
    
    hashed_password_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
    
    if bcrypt.checkpw(plain_text_password_bytes, hashed_password_bytes):
        return internal_response(data=True, success=True)
    else:
        return internal_response(success=False, message='Passwords do not match. From: check_password()')
    


def create_token(user_data):
        
        """
            Prepares a payload for encryption into a token format, use for authentication purposes.

            Args:
                user_data (dict): The user data to be encrypted and tokenised.

            Returns:
                token: The authentication token generated from the user_data supplied
            """  
        
        import datetime
        import jwt
        from build_response import internal_response

        payload = {
        'user_id': user_data['id'],
        'email': user_data['email'],
        'permissionLevel': user_data['role'],
        'exp': datetime.datetime.now(datetime.timezone.utc).timestamp() + 24 * 60 * 60
        }
        
        encryptedPayload = generate_encrypted_payload(payload)

        if encryptedPayload['success'] == True:
                
            new_payload = {'data': encryptedPayload['data']}

            secret_key = 'your-secret-key'

            token = jwt.encode(new_payload, secret_key, algorithm='HS256')

            return internal_response(data=token, success=True)
        else:
             return encryptedPayload
        
def decrypt_token(token):
    import json
    from jwcrypto import jwe, jwk
    from build_response import internal_response
    import jwt  # to decode the JWT

    # Step 1: Decode the JWT
    secret_key = 'your-secret-key'  # The same key used in create_token()
    
    try:
        # Decode the JWT to extract the encrypted JWE payload
        decoded_jwt = jwt.decode(token, secret_key, algorithms=['HS256'])

        # Retrieve the encrypted JWE payload from the JWT
        encrypted_payload = decoded_jwt.get('data')
        if not encrypted_payload:
            return internal_response(success=False, message='Encrypted payload not found in token.')

    except jwt.ExpiredSignatureError:
        return internal_response(success=False, message='Token has expired.')
    except jwt.InvalidTokenError as e:
        return internal_response(success=False, message=f'Invalid token: {str(e)}')

    # Step 2: Decrypt the JWE payload
    key_str_response = get_key()
    if key_str_response['success']:
        try:
            # Load the key JSON into a JWK object
            key_dict = json.loads(key_str_response['data'])
            key = jwk.JWK(**key_dict)

            # Create the JWE object and deserialize the encrypted payload
            jwetoken = jwe.JWE()
            jwetoken.deserialize(encrypted_payload)

            # Decrypt the token using the provided key
            jwetoken.decrypt(key)

            # Retrieve and parse the decrypted payload
            decrypted_payload = jwetoken.payload.decode('utf-8')
            decrypted_payload_dict = json.loads(decrypted_payload)

            # Return the decrypted data as an internal response
            return internal_response(data=decrypted_payload_dict, success=True)

        except Exception as e:
            return internal_response(success=False, message=f"Failed to decrypt payload. Error: {str(e)}")

    else:
        return internal_response(success=False, message='Failed to fetch secret key from DB. From: decrypt_token')
    
def verify_token(decrypted_payload):
    from db_access_functions import get_user_by_email
    from build_response import internal_response
    get_user_by_email_response = get_user_by_email(decrypted_payload['email'])
    if get_user_by_email_response['success']:
        import datetime
        if datetime.datetime.now(datetime.timezone.utc).timestamp() <= decrypted_payload['exp']:
            return internal_response(success=True, message='Token is valid')
        else:
            return internal_response(success=False, message='Token is not valid')

        
