from urllib.parse import urlencode

import requests

from typeform import exception
from typeform.enumerator import ErrorEnum


class Client(object):
    BASE_URL = 'https://api.typeform.com/'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None

    def authorization_url(self, redirect_uri, scope):
        params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'scope': ' '.join(scope)
        }
        return 'https://api.typeform.com/oauth/authorize?' + urlencode(params)

    def exchange_code(self, redirect_uri, code):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': redirect_uri
        }
        return self._post('oauth/token', data=data)

    def set_access_token(self, token):
        self.access_token = token

    @staticmethod
    def get_form_uid(form_url):
        """
        Returns addresses registered by the user.

        Args:
            form_url: String, Url from the form (the method needs the uid or form).

        Returns:
            A string.

        """
        return form_url.split('/to/')[-1]

    def get_form_information(self, form_uid=None, form_url=None):
        """
        Returns addresses registered by the user.

        Args:
            form_uid: Unique ID for the form.
            form_url: String, Url from the form (the method needs the uid or form).

        Returns:
            A dict.

        """
        if form_url:
            form_uid = self.get_form_uid(form_url)
        if not form_uid:
            raise Exception('You must provide either a Form UID or Form URL.')
        return self._get('forms/{}'.format(form_uid))

    def get_form_questions(self, form_uid=None, form_url=None, form=None):
        """
        Returns questions of form.

        Args:
            form_uid: Unique ID for the form.
            form_url: String, Url from the form (the method needs the uid or form).
            form:

        Returns:
            A dict.

        """
        if form:
            return form['fields']
        response = self.get_form_information(form_uid=form_uid, form_url=form_url)
        return response['fields']

    def get_form_metadata(self, form_uid, since, until):
        """
        Returns metadata of form (include answers).

        Args:
            form_uid: String, ID from the form.

            since: String,  The since parameter is a string that uses ISO 8601 format,
            Coordinated Universal Time (UTC), with "T" as a delimiter between the date and time.
            July 10, 2017 at 12:00 a.m. UTC is expressed as 2017-07-10T00:00:00.
            If you want to retrieve responses for yesterday, 2017-07-09, the value for your since query parameter
            would be 2017-07-09T00:00:00.

            until: String, The until parameter is a string that uses ISO 8601 format,
            Coordinated Universal Time (UTC), with "T" as a delimiter between the date and time.
            July 10, 2017 at 12:00 a.m. UTC is expressed as 2017-07-10T00:00:00.
            If you want to retrieve responses for yesterday, 2017-07-09, the value for your since query parameter
            would be 2017-07-09T00:00:00.

        Returns:
            A dict.

        """
        params = {
            'since': since,
            'until': until,
        }
        response = self._get("forms/{}/responses".format(form_uid), params=params)
        return response['items']

    def get_forms(self):
        """
        Returns all forms.

        Returns:
            A dict.

        """
        return self._get('forms')

    def create_webhook(self, webhook_url, form_uid, webhook_tag):
        """

        Args:
            webhook_url: String URL webhook request.
            form_uid: String, Unique ID for the form.
            webhook_tag: String.

        Returns:
            A dict.

        """
        data = {
            'url': webhook_url,
            'enabled': True
        }
        return self._put('forms/{}/webhooks/{}'.format(form_uid, webhook_tag), json=data)

    def view_webhook(self, form_uid, webhook_tag):
        """

        Args:
            form_uid: String, Unique ID for the form.
            webhook_tag: String.

        Returns:

        """
        return self._get('forms/{}/webhooks/{}'.format(form_uid, webhook_tag))

    def delete_webhook(self, form_uid, webhook_tag):
        """

        Args:
            form_uid: String, Unique ID for the form.
            webhook_tag: String.

        Returns:

        """
        return self._delete('forms/{}/webhooks/{}'.format(form_uid, webhook_tag))

    def _get(self, endpoint, **kwargs):
        return self._request('GET', endpoint, **kwargs)

    def _post(self, endpoint, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def _put(self, endpoint, **kwargs):
        return self._request('PUT', endpoint, **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)

    def _request(self, method, endpoint, **kwargs):
        headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
        response = requests.request(method, self.BASE_URL + endpoint, headers=headers, **kwargs)
        return self._parse(response)

    def _parse(self, response):
        if 'Content-Type' in response.headers and 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            try:
                r = response.json()
            except Exception:
                r = response.text

        if isinstance(r, dict) and 'code' in r and 'description' in r:
            message = r['description']
            code = r['code']
            try:
                error_enum = ErrorEnum(response.status_code)
            except Exception:
                raise exception.UnexpectedError('Error: {}. Message {}'.format(code, message))
            if error_enum == ErrorEnum.Forbidden:
                raise exception.Forbidden(message)
            if error_enum == ErrorEnum.Not_Found:
                raise exception.NotFound(message)
            if error_enum == ErrorEnum.Payment_Required:
                raise exception.PaymentRequired(message)
            if error_enum == ErrorEnum.Internal_Server_Error:
                raise exception.InternalServerError(message)
            if error_enum == ErrorEnum.Service_Unavailable:
                raise exception.ServiceUnavailable(message)
            if error_enum == ErrorEnum.Bad_Request:
                raise exception.BadRequest(message)
            if error_enum == ErrorEnum.Unauthorized:
                raise exception.Unauthorized(message)

        return r
