import sys
import yaml
import pyaml
from slugify import slugify

candidates = yaml.load(open(sys.argv[1]))

people = yaml.load(open(sys.argv[2]))

for region in candidates:
  for candidate in candidates[region]:
    name = unicode(candidate['name'])
    id = slugify(name)

    person = people.get(id, {})

    person['name'] = name
    person['id'] = id

    people[person['id']] = person

pyaml.dump(people, sys.stdout, vspacing=[2, 0])

