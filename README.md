# typeform-python
TypeForm API wrapper written in python.

## Installing
```
pip install git+git://github.com/GearPlug/typeform-python.git
```

## Requirements
- requests


## EndPoints
- base: The base endpoint response contains information about the API. It is useful for testing or making sure you have access.
- forms: The form endpoint is the main endpoint that you will be dealing with. It is the endpoint you use to create new typeforms. You have parameters to set the title, webhook URL and of course, the fields. The form endpoint will also return you a hash of URLs that you can use to distribute your typeform or delete it.
- images: Due to existing constraints, we cannot process all images on the fly when creating typeforms containing the 'Picture Choice' question type. Therefore, we provide an endpoint for creating images for Picture Choices before creating your typeform.
- designs: A design is what you see when you load your typeform. It contains information that is related to the styling of your typeform.
- urls: The url endpoint creates a new URL linking to a typeform.
