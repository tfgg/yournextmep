import sys
import requests
import json
import yaml

from local_settings import POPIT_USERNAME, POPIT_PASSWORD, POPIT_APIKEY

instance = "http://yournextmep.popit.mysociety.org/api/v0.1/"

instance_meta = requests.get(instance).json()

people_api_url = instance_meta['meta']['persons_api_url']
posts_api_url = instance_meta['meta']['posts_api_url']
memberships_api_url = instance_meta['meta']['memberships_api_url']

headers = {'content-type': 'application/json',
           'Apikey': POPIT_APIKEY}

def add_person(person):
  return requests.post(people_api_url,
                       data=json.dumps(person),
                       auth=(POPIT_USERNAME, POPIT_PASSWORD),
                       headers=headers)

def update_person(person):
  return requests.put(person['url'],
                     data=json.dumps(person),
                     auth=(POPIT_USERNAME, POPIT_PASSWORD),
                     headers=headers)

def delete_person(person):
  return requests.delete(person['url'],
                         auth=(POPIT_USERNAME, POPIT_PASSWORD),
                         headers=headers)

def add_membership(membership):
  return requests.post(memberships_api_url,
                       data=json.dumps(membership),
                       auth=(POPIT_USERNAME, POPIT_PASSWORD),
                       headers=headers)

def update_membership(membership):
  return requests.put(membership['url'],
                     data=json.dumps(membership),
                     auth=(POPIT_USERNAME, POPIT_PASSWORD),
                     headers=headers)

def delete_membership(membership):
  return requests.delete(membership['url'],
                         auth=(POPIT_USERNAME, POPIT_PASSWORD),
                         headers=headers)

def popitize(person, party_id, party):
  person = dict(person)

  person['identifiers'] = []
  person['identifiers'].append({'identifier': party_id + "/" + person['id'],
                                'scheme': 'yournextmep-candidate'})

  person['contact_details'] = []

  if 'email' in person:
    person['contact_details'].append({'type': 'email',
                                      'value': person['email'],})
    del person['email']

  if 'links' in person:
    for link in person['links']:
      if 'twitter' in link['url']:
        twitter_id = link['url'].split('/')[-1]

        person['contact_details'].append({'type': 'twitter',
                                          'value': twitter_id})

  if 'image' in person:
    image = {'url': "http://yournextmep.com" + person['image']}

    person['images'] = [image] 

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

def find_persons_id(person_id):
  url = instance + "search/persons?q=identifiers.identifier:\"{}\"".format(person_id)

  resp = requests.get(url).json()

  if len(resp['result']) > 1:
    print "MULTIPLE PEOPLE HITS", url

  if resp['result']:
    for person in resp['result']:
      for ident in person['identifiers']:
        if ident['scheme'] == "yournextmep-candidate" and ident['identifier'] == person_id:
          yield person
    
  return

def find_memberships_id(person_id, org_id):
  url = instance + "search/memberships?q=(person_id:\"{}\") AND (organization_id:\"{}\")".format(person_id, org_id)

  resp = requests.get(url).json()

  if len(resp['result']) > 1:
    print "MULTIPLE HITS", url

  if resp['result']:
    return resp['result']
    
  return None

def find_post(region_name):
  url = instance + "search/posts?q=label:\"Member of the European Parliament for {}\"".format(region_name)

  resp = requests.get(url).json()

  return resp['result'][0]

if __name__ == "__main__":
  party_id = sys.argv[1]
  candidates = yaml.load(open("_data/{}_candidates.yaml".format(party_id)))
  people = yaml.load(open("_data/{}_people.yaml".format(party_id)))
  regions = yaml.load(open("_data/regions.yaml"))

  party = find_org_id(party_id)

  for region_id, region_candidates in candidates.items():
    popit_post = find_post(regions[region_id]['name'])

    for candidate in region_candidates:
      person_id = candidate['id']

      person = people[person_id]
      person = popitize(person, party_id, party)

      print person_id

      popit_persons = list(find_persons_id(party_id + "/" + person_id))

      if not popit_persons:
        print "  Adding"
        resp = add_person(person)
      else:
        for popit_person in popit_persons[1:]:
          print "Deleting duplicate person"
          delete_person(popit_person)

        popit_person = popit_persons[0]
        print "  Updating", popit_person['url']
        popit_person.update(person)
        resp = update_person(popit_person)

      #popit_person = find_person_id(party_id + "/" + person_id)
      popit_person = resp.json()['result']
     
      popit_memberships = find_memberships_id(popit_person['id'], party['id'])

      if popit_memberships:
        for popit_membership in popit_memberships[1:]:
          print "Deleting membership"
          delete_membership(popit_membership)

      membership = {
        "label": "European electoral candidate for {}".format(regions[region_id]['name']),
        "role": "candidate",
        "post_id": popit_post['id'],
        "person_id": popit_person['id'],
        "organization_id": party['id'],
      }

      if popit_memberships is None:
        print "Adding membership"
        resp = add_membership(membership) 
      else:
        print "Updating membership"
        popit_membership = popit_memberships[0]
        membership['id'] = popit_membership['id']
        membership['url'] = popit_membership['url']
        resp = update_membership(membership)
      
      print resp.status_code

