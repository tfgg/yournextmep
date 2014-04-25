import sys
import yaml
import pyaml
from slugify import slugify

candidates = yaml.load(open(sys.argv[1]))

try:
  people = yaml.load(open(sys.argv[2]))
except:
  people = {}

for region in candidates:
  for candidate in candidates[region]:
    name = unicode(candidate['name'])
    id = candidate['id']

    person = people.get(id, {})

    person['name'] = name
    person['id'] = id

    people[person['id']] = person

pyaml.dump(people, open(sys.argv[2],'w+'), vspacing=[2, 0])

