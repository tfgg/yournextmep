import sys
import yaml
import pyaml
from slugify import slugify

candidates = yaml.load(open(sys.argv[1]))

people = {}

for region in candidates:
  for candidate in candidates[region]:
    person = {'name': candidate['name'],
              'id': slugify(candidate['name']),}

    if 'wikipedia' in candidate:
      person['links'] = [{'note': 'Wikipedia article',
                          'url': candidate['wikipedia'],}]

    people[person['id']] = person

pyaml.dump(people, sys.stdout, vspacing=[2, 0])

