import os
from unittest import TestCase
from typeform.client import Client, ClientAuth
from datetime import datetime, timedelta


class TypeformTestCases(TestCase):
    def setUp(self):
        self.access_token = os.environ.get('token')
        self.api_key = os.environ.get('apikey')
        self.form_id = os.environ.get('form_id')
        self.url_webhook = os.environ.get('url_webhook')
        self.client=Client(access_token=self.access_token)

    def test_create_webhook(self):
        result_create = self.client.create_webhook(url_webhook=self.url_webhook,uid=self.form_id, tag_webhook=1)
        result_view = self.client.view_webhook(tag_webhook=1, uid=self.form_id)
        self.client.delete_webhook(tag_webhook=1, uid=self.form_id)
        self.assertEqual(result_create['id'],result_view['id'])

    def test_delete_webhook(self):
        result_create = self.client.create_webhook(url_webhook=self.url_webhook,uid=self.form_id, tag_webhook=1)
        self.client.delete_webhook(tag_webhook=1, uid=self.form_id)
        try:
            result_view = self.client.view_webhook(tag_webhook=1, uid=self.form_id)
            result = False
        except:
            result = True
        self.assertTrue(result)

    def test_get_forms(self):
        result = self.client.get_forms()
        _form = ""
        for r in result['items']:
            if r['id'] == self.form_id:
                _form = r['id']
        self.assertEqual(_form, self.form_id)

    def test_get_form_information(self):
        result = self.client.get_form_information(uid=self.form_id)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['id'], self.form_id)

    def test_get_form_questions(self):
        result = self.client.get_form_questions(uid=self.form_id)
        self.assertIsInstance(result, list)
        self.assertIn('title', result[0])

    def test_get_form_metadata(self):
        since = (datetime.utcnow() - timedelta(days=1)).isoformat()
        until = datetime.utcnow().isoformat()
        result = self.client.get_form_metadata(uid=self.form_id, since=since, until=until)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0],dict)
        self.assertIn('answers', result[0])






