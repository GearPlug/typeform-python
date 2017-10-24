import requests
from requests.auth import AuthBase
from typeform import exception
from typeform.enumerator import ErrorEnum
from typeform.clientauth import ClientAuth
import json

class Client(object):
    _VALID_VERSIONS = ['v1']

    def __init__(self, api_key=None, access_token=None, version=None):
        self.access_token = access_token
        self.api_key = api_key
        if version not in self._VALID_VERSIONS:
            self.version = self._VALID_VERSIONS[0]
        if api_key:
            self.auth = ClientAuth(api_key=api_key)
            self.base_url = 'https://api.typeform.com/'+self._VALID_VERSIONS[0]
        elif access_token:
            self.auth = ClientAuth(access_token=access_token)
            self.base_url = 'https://api.typeform.com'
        else:
            raise exception.CredentialRequired("You must provide either access_token or api_key")

    def _get(self, endpoint, data=None):
        return self._request('GET', endpoint, data=data)

    def _put(self, endpoint, data=None):
        return self._request('PUT', endpoint, data=data)

    def _delete(self, endpoint, data=None):
        return self._request('DELETE', endpoint, data=data)

    def _request(self, method, endpoint, data=None):
        url = '{0}/{1}'.format(self.base_url, endpoint)
        response = requests.request(method, url, auth=self.auth, data=json.dumps(data))
        return self._parse(response)

    def _parse(self, response):
        if not response.ok:
            try:
                data = response.json()
                if 'description' in data and 'code' in data:
                    message = data['description']
                    code = data['code']
            except:
                code = response.status_code
                message = ""
            try:
                error_enum = ErrorEnum(response.status_code)
            except Exception:
                raise exception.UnexpectedError('Error:{0}{1}.Message{2}'.format(code, response.status_code, message))
            if error_enum == ErrorEnum.Forbidden:
                raise exception.Forbidden(message)
            if error_enum == ErrorEnum.Not_Found:
                raise exception.Not_Found(message)
            if error_enum == ErrorEnum.Payment_Required:
                raise exception.Payment_Required(message)
            if error_enum == ErrorEnum.Internal_Server_Error:
                raise exception.Internal_Server_Error(message)
            if error_enum == ErrorEnum.Service_Unavailable:
                raise exception.Service_Unavailable(message)
            if error_enum == ErrorEnum.Bad_Request:
                raise exception.Bad_Request(message)
            if error_enum == ErrorEnum.Unauthorized:
                raise exception.Unauthorized(message)
            else:
                raise exception.BaseError('Error: {0}{1}. Message {2}'.format(code, response.status_code, message))
            return data
        else:
            return response

    def get_form_uid(self, url_form):
        """Returns addresses registered by the user.
        Args:
            url_form: String, Url from the form (the method needs the uid or form)
        Returns:
            A string.
        """
        list_url = url_form.split("/to/")
        typeform_uid = list_url[1]
        return typeform_uid

    def get_form_information(self, uid=None, url=None):
        """Returns addresses registered by the user.
        Args:
            uid: Unique ID for the form
        Returns:
            A dict.
        """
        if uid is None:
            if url is None:
                raise Exception('You must provide either an UID or Form URL.')
            else:
                uid = self.get_form_uid(url)
        return self._get('forms/{}'.format(uid)).json()

    def get_form_questions(self, uid=None, url=None, form=None):
        """Returns questions of form.
        Args:
            uid: Unique ID for the form
            url: String, Url from the form (the method needs the uid or form)
        Returns:
            A dict.
        """
        if form is not None:
            return form['fields']
        return self.get_form_information(uid=uid, url=url)['fields']

    def get_form_metadata(self, since, until, uid=None, url=None, form=None):
        """Returns metadata of form (include answers).
        Args:
            uid: String, ID from the form
            url: String, Url from the form (the method needs the uid or form)
            form: String, A form
            since: String,  The since parameter is a string that uses ISO 8601 format,
            Coordinated Universal Time (UTC), with "T" as a delimiter between the date and time.
            July 10, 2017 at 12:00 a.m. UTC is expressed as 2017-07-10T00:00:00.
            If you want to retrieve responses for yesterday, 2017-07-09, the value for your since query parameter
            would be 2017-07-09T00:00:00
            until: String, The until parameter is a string that uses ISO 8601 format,
            Coordinated Universal Time (UTC), with "T" as a delimiter between the date and time.
            July 10, 2017 at 12:00 a.m. UTC is expressed as 2017-07-10T00:00:00.
            If you want to retrieve responses for yesterday, 2017-07-09, the value for your since query parameter
            would be 2017-07-09T00:00:00
        Returns:
            A dict.
        """
        if form is not None:
            return form['responses']
        data = {
            'since': since,
            'until': until,
        }
        return self._get(endpoint="forms/{0}/responses".format(uid), data=data).json()['items']


    def get_forms(self):
        """Returns all forms
        Args:
        Returns:
            A dict.
        """
        return self._get(endpoint='forms').json()

    def create_webhook(self, url_webhook, tag_webhook, uid):
        """
        :param url_webhook: String URL webhook request
        :param tag_webhook: String
        :param uid: String, Unique ID for the form
        :return: dict
        """
        if self.access_token is not None:
            data = {'url':url_webhook, 'enabled':True}
            return self._put(endpoint='forms/{1}/webhooks/{0}'.format(tag_webhook, uid), data=data).json()
        else:
            raise exception.TokenRequired("You need an access token for this method")

    def view_webhook(self, tag_webhook, uid):
        """
        :param tag_webhook: String
        :param uid: String, Unique ID for the form
        :return:
        """
        if self.access_token is not None:
            return self._get(endpoint='forms/{1}/webhooks/{0}'.format(tag_webhook, uid)).json()
        else:
            raise exception.TokenRequired("You need an access token for this method")

    def delete_webhook(self, tag_webhook, uid):
        """
        :param tag_webhook: String
        :param uid: String, Unique ID for the form
        :return:
        """
        if self.access_token is not None:
            return self._delete(endpoint='forms/{1}/webhooks/{0}'.format(tag_webhook, uid)).ok
        else:
            raise exception.TokenRequired("You need an access token for this method")