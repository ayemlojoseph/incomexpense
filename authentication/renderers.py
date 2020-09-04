from rest_framework import renderers
import json

#this helps in the documentations to show if its error or data 
#for example the json field that a result is return wonnt be just the data but rather with error tag or data tag


class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({'data': data})
        return response
#remember to map to any view you want to use it on
#personnaly i dont even see the use of this 
#import it before using with the view