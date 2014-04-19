import yaml
import csv

parties = yaml.load(open('_data/parties.yaml'))

out = open('candidates.csv', 'wb+')

print >>out, u"# Party Region Candidate Twitter".encode('utf-8')

for _, party in parties.items():
  candidates = yaml.load(open('_data/{}_candidates.yaml'.format(party['id'])))
  people = yaml.load(open('_data/{}_people.yaml'.format(party['id'])))

  for region, region_candidates in candidates.items():
    for candidate in region_candidates:
      person = people[candidate['id']]

      twitter_account = ""

      if 'links' in person:
        for link in person['links']:
          if 'Twitter account' == link['note']:
            twitter_account = link['url'].split('/')[-1]

      print >>out, u"{party_name}, {region_name}, {candidate_name}, {twitter_account}".format(party_name=party['name'],
                                                                   region_name=region,
                                                                   candidate_name=person['name'],
                                                                   twitter_account=twitter_account).encode('utf-8')

