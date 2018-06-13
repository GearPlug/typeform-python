import os
from datetime import datetime, timedelta
from unittest import TestCase

from typeform.client import Client


class TypeformTestCases(TestCase):
    def setUp(self):
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.access_token = os.environ.get('ACCESS_TOKEN')
        self.form_id = os.environ.get('FORM_ID')
        self.webhook_url = os.environ.get('WEBHOOK_URL')
        self.client = Client(self.client_id, self.client_secret)
        self.client.set_access_token(self.access_token)

    def test_create_webhook(self):
        result_create = self.client.create_webhook(webhook_url=self.webhook_url, form_uid=self.form_id, webhook_tag=1)
        result_view = self.client.view_webhook(form_uid=self.form_id, webhook_tag=1)
        self.client.delete_webhook(form_uid=self.form_id, webhook_tag=1)
        self.assertEqual(result_create['id'], result_view['id'])

    def test_delete_webhook(self):
        result_create = self.client.create_webhook(webhook_url=self.webhook_url, form_uid=self.form_id, webhook_tag=1)
        self.client.delete_webhook(webhook_tag=1, form_uid=self.form_id)
        result_view = self.client.view_webhook(form_uid=self.form_id, webhook_tag=1)
        self.assertFalse(result_view)

    def test_get_forms(self):
        result = self.client.get_forms()
        _form = ""
        for r in result['items']:
            if r['id'] == self.form_id:
                _form = r['id']
        self.assertEqual(_form, self.form_id)

    def test_get_form_information(self):
        result = self.client.get_form_information(form_uid=self.form_id)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['id'], self.form_id)

    def test_get_form_questions(self):
        result = self.client.get_form_questions(form_uid=self.form_id)
        self.assertIsInstance(result, list)
        self.assertIn('title', result[0])

    def test_get_form_metadata(self):
        since = (datetime.utcnow() - timedelta(days=1)).isoformat()
        until = datetime.utcnow().isoformat()
        result = self.client.get_form_metadata(form_uid=self.form_id, since=since, until=until)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        self.assertIn('answers', result[0])
