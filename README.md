# typeform-python
TypeForm API wrapper written in python.

## Installing
```
pip install typeform-python
```

## Usage
```
from typeform.client import Client

client = Client('CLIENT_KEY', 'CLIENT_SECRET')
```

Get authorization url
```
url = client.authorization_url('REDIRECT_URI', ['forms:write', 'forms:read'])
```

Exchange the code for a token
```
token = client.exchange_code('REDIRECT_URI', 'CODE')
```

Set the token
```
client.set_access_token('TOKEN')
```

Get form ID
```
client.get_form_uid('FORM_URL')
```

Get form information
```
client.get_form_information('FORM_UID')
```

Get form questions
```
client.get_form_questions('FORM_UID')
```

Get form metadata
```
client.get_form_metadata('FORM_UID', 'SINCE', 'UNTIL')
```

Get all forms
```
client.get_forms()
```

Create Webhook
```
client.create_webhook('WEBHOOK_URL', 'WEBHOOK_TAG', 'FORM_UID')
```

View Webhook
```
client.view_webhook('WEBHOOK_TAG', 'FORM_UID')
```

Delete Webhook
```
client.delete_webhook('WEBHOOK_TAG', 'FORM_UID')
```

## Requirements
- requests

## TODO
- create_form
- Update_form
- delete_form
- get_custom_form_messages
- update_custom_messages
- create_image
- get_images_collection
- get_image
- delete_image
- get_image_by_size
- get_background_by_size
- get_choice_image_by_size
- create_theme
- get_themes
- update_themes
- delete_themes
