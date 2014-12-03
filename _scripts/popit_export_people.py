import sys
import requests
import json
import yaml

from local_settings import POPIT_USERNAME, POPIT_PASSWORD

instance = "http://yournextmep.popit.mysociety.org/api/v0.1/"

instance_meta = requests.get(instance).json()

people_api_url = instance_meta['meta']['persons_api_url']
memberships_api_url = instance_meta['meta']['memberships_api_url']

def add_person(person):
  print person
  return requests.post(people_api_url,
                       data=json.dumps(person),
                       auth=(POPIT_USERNAME, POPIT_PASSWORD),
                       headers={'content-type': 'application/json'})

def update_person(person):
  return requests.put(person['url'],
                     data=json.dumps(person),
                     auth=(POPIT_USERNAME, POPIT_PASSWORD),
                     headers={'content-type': 'application/json'})


def add_membership(membership):
  return requests.post(memberships_api_url,
                       data=json.dumps(membership),
                       auth=(POPIT_USERNAME, POPIT_PASSWORD),
                       headers={'content-type': 'application/json'})

def update_membership(membership):
  return requests.put(membership['url'],
                     data=json.dumps(membership),
                     auth=(POPIT_USERNAME, POPIT_PASSWORD),
                     headers={'content-type': 'application/json'})

def delete_membership(membership):
  return requests.delete(membership['url'],
                         auth=(POPIT_USERNAME, POPIT_PASSWORD),
                         headers={'content-type': 'application/json'})

def popitize(person, party_id, party):
  person = dict(person)

  person['identifiers'] = []
  person['identifiers'].append({'identifier': party_id + "/" + person['id'],
                                'scheme': 'yournextmep'})

  if 'image' in person:
    person['image'] = "http://yournextmep.com" + person['image']

  del person['id']

  return person

def find_org_id(org_id):
  url = instance + "search/organizations?q=identifiers.identifier:\"{}\"".format(org_id)

  resp = requests.get(url).json()

  if resp['result']:
    for org in resp['result']:
      for ident in org['identifiers']:
        if ident['scheme'] == "yournextmep" and ident['identifier'] == org_id:
          return org
    
  return None

def find_person_id(person_id):
  url = instance + "search/persons?q=identifiers.identifier:\"{}\"".format(person_id)

  resp = requests.get(url).json()

  print url

  if len(resp['result']) > 1:
    print "MULTIPLE HITS", url

  if resp['result']:
    for org in resp['result']:
      for ident in org['identifiers']:
        if ident['scheme'] == "yournextmep" and ident['identifier'] == person_id:
          return org
    
  return None


def find_membership_id(person_id, org_id):
  url = instance + "search/memberships?q=(person_id:\"{}\") AND (organization_id:\"{}\")".format(person_id, org_id)

  resp = requests.get(url).json()

  if len(resp['result']) > 1:
    print "MULTIPLE HITS", url

  if resp['result']:
    return resp['result'][0]
    
  return None

if __name__ == "__main__":
  party_id = sys.argv[1]
  candidates = yaml.load(open("_data/{}_candidates.yaml".format(party_id)))
  people = yaml.load(open("_data/{}_people.yaml".format(party_id)))
  regions = yaml.load(open("_data/regions.yaml"))

  party = find_org_id(party_id)

  for region_id, region_candidates in candidates.items():
    for candidate in region_candidates:
      person_id = candidate['id']

      person = people[person_id]
      person = popitize(person, party_id, party)

      popit_person = find_person_id(party_id + "/" + person_id) 

      if popit_person is None:
        print "  Adding"
        resp = add_person(person)
        print resp.status_code, resp.text
      else:
        print "  Already up", popit_person['url']
        #resp = update_person(popit_person)


      popit_person = find_person_id(party_id + "/" + person_id) 
      
      popit_membership = find_membership_id(popit_person['id'], party_id) 

      if popit_membership is not None:
        delete_membership(popit_membership)

      popit_membership = find_membership_id(popit_person['id'], party['id']) 

      print popit_membership

      membership = {
        "label": "European electoral candidate for {}".format(regions[region_id]['name']),
        "role": "European electoral candidate",
        "person_id": popit_person['id'],
        "organization_id": party['id'],
        "area": {"name": regions[region_id]['name'],
                 "classification": "EUR",
                 "id": "mapit.mysociety.org/area/{}".format(regions[region_id]['identifiers'][0]['identifier'])}
      }

      if popit_membership is None:
        resp = add_membership(membership) 
      else:
        membership['id'] = popit_membership['id']
        membership['url'] = popit_membership['url']
        resp = update_membership(membership)
      
      print resp.status_code, resp.text

