import sys
from grab_dbpedia import get_comment
import yaml, pyaml

people = yaml.load(open(sys.argv[1]))

def get_wikipedia_id(wikipedia_url):
  return wikipedia_url.split('/')[-1]

for person_id in people:
  person = people[person_id]

  if 'links' in person:
    for link in person['links']:
      if 'wikipedia' in link['url']:
        wikipedia_id = get_wikipedia_id(link['url'])
        try:
          comment = get_comment(wikipedia_id)
          if comment is not None:
            person['wikipedia_biography'] = comment['value']
        except Exception, e:
          print e

f = open(sys.argv[1], 'w+')
pyaml.dump(people, f, vspacing=[2,0])
f.close()

