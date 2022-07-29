import requests
import pandas as pd
import json
import time

JUPITER_KEY = #Insert Jupiter Key
JUPITER_URL = #Insert Jupiter URL

print('Accessing credentials...')

### Credentials ###
dict_login = {
    'riodejaneiro-br': {
        'credentials': {
            'loginId': 'username',
            'password': 'password'
        }
        , 'x-api-key': 'Insert x-api-key for authentication'
    }
}

dict_token = {}
dict_taskId = {}

print('Generating report...')

### Authentication ###
for key, value in dict_login.items():
    credentials = value['credentials']
    praca = key
    print("Reading dictionary")
    print(key, credentials['loginId'], credentials['password'])

    url_login = f'URL login'
    headers = {
        'content-type': 'application/json',
        'x-api-key': value['x-api-key'],
        'x-sg-url': 'Business Unit Link',
        'x-sg-authorization': JUPITER_KEY
    }

    print('Getting token...')

    r_login = requests.post(url_login, data=json.dumps(credentials), headers=headers)
    token = r_login.json().get('token')
    print(f'R_LOGIN - Token: {r_login.text}')
    dict_token[praca] = token
    time.sleep(1)

    headers_download = {
        'content-type': 'application/json',
        'x-api-key': value['x-api-key'],
        'x-auth-token': dict_token[praca],
        'x-sg-url': 'Business Unit URL',
        'x-sg-authorization': JUPITER_KEY
    }
    
    url_controle = (
        f'Export Link')
    r_download = requests.get(url_controle, data=json.dumps(credentials), headers=headers_download)
    jaison_taskId = r_download.json().get('taskId')
    dict_taskId[praca] = jaison_taskId
    print(f'R_DOWNLOAD: {r_download.text}')
    time.sleep(5)

print('Waiting 25 seconds to extract report...')
time.sleep(25)


print('Extracting report...')

### Export Bikes in Maintenance ###
for chave, value in dict_login.items():
    praca = chave
    credentials = value['credentials']
    headers_taskId = {
        'content-type': 'text/csv',
        'x-api-key': value['x-api-key'],
        'x-auth-token': dict_token[praca],
        'x-sg-url': f'https://{praca}.cometlink',
        'x-sg-authorization': JUPITER_KEY
    }

    url_tasks = (f'business_unit_link{dict_taskId[praca]}/result')
    r_tasks = requests.get(url_tasks, data=json.dumps(credentials), headers=headers_taskId)
    print(f'Generating file bikes_in_maintenance_{praca}.csv')
    f = open(f'bikes_in_maintenance_{praca}.csv', 'w')
    f.write(r_tasks.content.decode("utf-8"))
    f.close()
    rawData = pd.read_csv(f'bikes_in_maintenance_{praca}.csv', encoding='ISO-8859-1')
    print(rawData.head(3))

print('Report extracted successfully')

print('Iniciando checkup...')

### Starting Checkup ###
countid = rawData['id'].count()

for id in rawData['id']:
    url_checkup = (f'business_unit_link{id}/checkup')
    r_checkup = requests.post(url_checkup, data=json.dumps(credentials), headers=headers_download)
    print(f'{url_checkup}')
    print(r_checkup)
print('{} bikes bikes checked successfully!'.format((countid)))

print('Checkup completed!')
