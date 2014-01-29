import yaml, pyaml
import sys
from slugify import slugify

candidates = yaml.load(open(sys.argv[1]))

for region in candidates:
  for candidate in candidates[region]:
    candidate['id'] = slugify(candidate['name'])

f = open(sys.argv[1], 'w+')
pyaml.dump(candidates, f, vspacing=[2, 0])
f.close()

