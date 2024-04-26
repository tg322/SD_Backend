
"""
    Retrieves the secret key for encryption.

    Returns:
        .encrypt_key object for use when encrypting.
    """




def get_key():

    from build_response import internal_response

    from db_models import encryption_key
    key_data = encryption_key.query.first()
    if key_data:
        print(key_data)
        return internal_response(data=key_data.encrypt_key, success=True)
    else:
        return internal_response(success=False, message='Failed to fetch secret key from DB. From: get_key()')
    
def generate_encrypted_payload(payload):
    from build_response import internal_response
    import json
    from jwcrypto import jwe, jwk
    import jwt

    payload_str = json.dumps(payload)
    key_str_response = get_key()

    # Correct way to access dictionary keys
    if key_str_response['success'] == True:
        # Assuming the key is stored correctly as a dict; if it's a simple string, this needs adjustment
        key = jwk.JWK.from_json(key_str_response['data'])  # Adjusted for typical JWK usage

        jwetoken = jwe.JWE(plaintext=payload_str.encode('utf-8'),
                           protected={"alg": "A256KW", "enc": "A256CBC-HS512"})
        jwetoken.add_recipient(key)
        encrypted_payload = jwetoken.serialize(compact=True)

        return internal_response(data=encrypted_payload, success=True)
    else:
        return key_str_response