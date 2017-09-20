# typeform-python
TypeForm API wrapper written in python.

## Installing
```
pip install git+git://github.com/GearPlug/typeform-python.git
```

## Requirements
- requests


## Usage
```
from typeform.client import Client

client = Client('API_KEY')
```

Get form ID
```
client.get_form_uid('URL_FORM')
```

Get form information
```
client.get_form_information('UID, URL')
```

Get form stats
```
client.get_form_stats('UID, URL')
```

Get form questions
```
client.get_form_questions('UID, URL')
```

Get form metadata
```
client.get_form_metadata('UID, URL')
```

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
