import sys
import yaml

people = yaml.load(open(sys.argv[1]))

def get_twitter_id(twitter_url):
  return twitter_url.split('/')[-1]

for person_id, person in people.items():
  if 'links' in person:
    for link in person['links']:
      if 'twitter' in link['url']:
        print person_id, get_twitter_id(link['url'])

