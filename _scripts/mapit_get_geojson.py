import yaml
import sys
import requests
import time

data = yaml.load(open(sys.argv[1]))

#tolerance = 0.0001
tolerance = 0.01

for _, region in data.items():
  for identifier in region['identifiers']:
    if identifier['scheme'] == 'mapit':
      mapit_id = identifier['identifier']

      print mapit_id

      url = "http://mapit.mysociety.org/area/{}.geojson?simplify_tolerance={}".format(mapit_id, tolerance)
      resp = requests.get(url)
      geojson = resp.text

      print >>open('geojson/{}.geojson'.format(mapit_id), 'w+'), geojson

      time.sleep(1)

