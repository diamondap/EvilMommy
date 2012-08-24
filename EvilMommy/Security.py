import uuid, base64
from Crypto.Cipher import ARC4  # this is from pycrypto


class Security:
    """
    This class implements some basic security mechanisms so we can
    encrypt and decrypt the auth cookie and anything else we might
    consider sensitive.
    """

    def __init__(self, encryption_key):
        # Just store the key. We have to create a new instance of
        # ARC4 every time we encrypt or decrypt.
        self.key = encryption_key

    def create_auth_token(self, user_name, remote_addr):
        """
        Creates a base64-encoded encrypted string with our user's
        name and remote address. We can use this as an auth token
        in a cookie. We throw in a uuid so the the encrypted string
        looks different each time. We add the user's remote address
        to prevent others from swiping the cookie.
        """
        token = str(uuid.uuid4()) + "|" + user_name + "|" + remote_addr
        return base64.b64encode(ARC4.new(self.key).encrypt(token))

    def unpack_auth_token(self, token):
        """
        Unpacks the auth token from the cookie. Returns a dictionary
        with keys user_name and remote_addr.
        """
        try:
            decrypted = ARC4.new(self.key).decrypt(base64.b64decode(token))
            uuid, user_name, remote_addr = decrypted.split("|")
            return { 'user_name': user_name, 'remote_addr': remote_addr }
        except:
            return None


    def is_valid_user(self, token, user_list, remote_addr):
        """
        Returns true if the auth token shows that this is a valid
        user coming from the remote address they originally logged
        in from.
        """
        auth_data = self.unpack_auth_token(token)
        return (auth_data is not None and
                auth_data['user_name'] in user_list and
                auth_data['remote_addr'] == remote_addr)
