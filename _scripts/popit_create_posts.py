import sys
import requests
import json
import yaml

from local_settings import POPIT_USERNAME, POPIT_PASSWORD, POPIT_APIKEY

instance = "http://yournextmep.popit.mysociety.org/api/v0.1/"

instance_meta = requests.get(instance).json()

organizations_api_url = instance_meta['meta']['organizations_api_url']
posts_api_url = instance_meta['meta']['posts_api_url']

headers = {'content-type': 'application/json',
           'Apikey': POPIT_APIKEY}

def get_or_create_eup():
  url = instance + "search/organizations?q=name:\"European Parliament\""

  resp = requests.get(url).json()

  if resp['result']:
    return resp['result'][0]

  eup = {u'name': u'European Parliament',
         u'classification': u'Parliament'} 

  resp = requests.post(organizations_api_url,
                       data=json.dumps(eup),
                       auth=(POPIT_USERNAME, POPIT_PASSWORD),
                       headers=headers)
  
  return resp.json()['result']

def get_or_create_post(post):
  url = instance + "search/posts?q=label:\"{}\"".format(post['label'])
  resp = requests.get(url).json()

  if resp['result']:
    return resp['result'][0]
  else:
    resp = requests.post(posts_api_url,
                        data=json.dumps(post),
                        auth=(POPIT_USERNAME, POPIT_PASSWORD),
                        headers=headers)
  
    return resp.json()['result']

eup = get_or_create_eup()

regions = yaml.load(open('_data/regions.yaml'))

for _, region in regions.items():
  print region['name']

  post = {'organization_id': eup['id'],
          'role': 'Member of the European Parliament',
          'label': 'Member of the European Parliament for {}'.format(region['name']),
          "area": {
            "identifier": "http://mapit.mysociety.org/area/{}".format(region['identifiers'][0]['identifier']),
            "id": "mapit:{}".format(region['identifiers'][0]['identifier']),
            "name": region['name']
            },
          }

  post = get_or_create_post(post)

  print post

