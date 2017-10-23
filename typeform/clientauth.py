import requests
from typeform import exception

class ClientAuth(requests.auth.AuthBase):

    def __init__(self, access_token=None, api_key=None):
        if access_token:
            self.access_token = access_token
            self.api_key = None
        elif api_key:
            self.api_key = api_key
            self.access_token = None
        else:
            raise exception.CredentialRequired("You must provide either access_token or api_key")

    def __call__(self, r):
        if self.access_token is not None:
            r.headers['Authorization'] = 'bearer {0}'.format(self.access_token)
        elif self.api_key is not None:
            r.prepare_url(r.url, {'key': self.api_key})
        return r