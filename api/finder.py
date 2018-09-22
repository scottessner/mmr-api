import os
import requests

for root, dirs, files in os.walk('/data/mmr-prod/incoming/sheldon/tvshows'):

    for file in files:
        if os.path.splitext(file)[1] == '.ts':
            resp = requests.post('http://127.0.0.1:5000/api/job',
                                 json={'folder': root,
                                       'file_name': file,
                                       'full_path': os.path.join(root,file)})

            if resp.status_code == 201:
                print('Added: {}'.format(file))
            elif resp.status_code == 400:
                print('Not added: {}'.format(file))