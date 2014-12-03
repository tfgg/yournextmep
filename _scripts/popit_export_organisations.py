import sys
import requests
import json
import yaml

from local_settings import POPIT_USERNAME, POPIT_PASSWORD

instance = "http://yournextmep.popit.mysociety.org/api/v0.1/"

instance_meta = requests.get(instance).json()

organisations_api_url = instance_meta['meta']['organizations_api_url']

def add_organisation(org):
  print org
  return requests.post(organisations_api_url,
                       data=json.dumps(org),
                       auth=(POPIT_USERNAME, POPIT_PASSWORD),
                       headers={'content-type': 'application/json'})

def update_organisation(org):
  print org
  return requests.put(org['url'],
                     data=json.dumps(org),
                     auth=(POPIT_USERNAME, POPIT_PASSWORD),
                     headers={'content-type': 'application/json'})

def format_date(s):
  xs = map(int, s.split("-"))
  
  if len(xs) == 1:
    return "{0:04d}".format(*xs)
  elif len(xs) == 2:
    return "{0:04d}-{1:02d}".format(*xs)
  elif len(xs) == 3:
    return "{0:04d}-{1:02d}-{2:02d}".format(*xs)

def popitize(org):
  org = dict(org)

  org['identifiers'] = []
  org['identifiers'].append({'identifier': org['id'],
                             'scheme': 'yournextmep'})

  if 'founding_date' in party:
    org['founding_date'] = format_date(str(org['founding_date']))

  if 'image' in party:
    org['image'] = "http://yournextmep.com" + org['image']

  org['type'] = "Party"

  del org['id']

  return org

def find_org_id(org_id):
  url = instance + "search/organizations?q=identifiers.identifier:\"{}\"".format(org_id)

  print url

  resp = requests.get(url).json()

  if resp['result']:
    for org in resp['result']:
      for ident in org['identifiers']:
        if ident['scheme'] == "yournextmep" and ident['identifier'] == org_id:
          return org
    
  return None

if __name__ == "__main__":
  parties = yaml.load(open("_data/parties.yaml"))

  for party_id, party in parties.items():
    print party_id

    party = popitize(party)

    popit_doc = find_org_id(party_id)

    if popit_doc is None:
      print "  Adding"
      resp = add_organisation(party)
      print resp.status_code, resp.text
    else:
      print "  Already up", popit_doc['url']

      popit_doc.update(party)

      resp = update_organisation(popit_doc)

      print resp.status_code, resp.text
