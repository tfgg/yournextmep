import sys, os
import yaml
from slugify import slugify

party = sys.argv[1]

candidates = yaml.load(open("_data/{}_candidates.yaml".format(party)))
people = yaml.load(open("_data/{}_people.yaml".format(party)))

for region in candidates:
  for i, candidate in enumerate(candidates[region]):
    person_id = slugify(unicode(candidate['name']))
    rank = i

    s = """---
layout: candidate
permalink: candidates/eu2014/{}/{}/
categories: candidate {}
election: eu2014
list-rank: {}
person: {}
region: {}
party: {}
---""".format(party, person_id, party, rank, person_id, region, party)

    dir_path = os.path.join("_candidates", "eu2014", party)
    if not os.path.isdir(dir_path):
      os.mkdir(dir_path)

    path = os.path.join(dir_path, "{}.md".format(person_id))

    #print path
    #print s

    print >>open(path, "w+"), s
