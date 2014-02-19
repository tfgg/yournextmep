import yaml
import sys
import requests
import time

data = yaml.load(open(sys.argv[1]))

for _, region in data.items():
  for identifier in region['identifiers']:
    if identifier['scheme'] == 'mapit':
      mapit_id = identifier['identifier']

      print mapit_id

      url = "http://mapit.mysociety.org/area/{}.geojson".format(mapit_id)
      resp = requests.get(url)
      geojson = resp.json()

      print >>open('geojson/{}.geojson'.format(mapit_id), 'w+'), geojson

      time.sleep(1)

