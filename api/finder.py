import os
import requests

for root, dirs, files in os.walk('/run/user/1000/gvfs/smb-share:server=192.168.40.10,share=media/tvshows'):

    for file in files:
        if os.path.splitext(file)[1] == '.ts':
            resp = requests.post('http://ssessner.com/api/job',
                                 json={'folder': root,
                                       'file_name': file,
                                       'full_path': os.path.join(root,file)})

            if resp.status_code == 201:
                print('Added: {}'.format(file))
            elif resp.status_code == 400:
                print('Not added: {}'.format(file))