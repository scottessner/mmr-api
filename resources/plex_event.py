from flask_restful import Resource, request
import json

class PlexEvent(Resource):

    def post(self):
        req_data = json.loads(request.form['payload'])

        title = req_data['Metadata'].get(['title'], '')
        parent_title = req_data['Metadata'].get(['parentTitle'], '')
        grandparent_title = req_data['Metadata'].get(['grandparentTitle'], '')

        print('POST event: {}\n\t\t{}\n\t\t{}\n\t\t{}'.format(req_data['event'],
                                                              grandparent_title,
                                                              parent_title,
                                                              title))

    def get(self):
        req_data = request.get_json()
        print('GET')