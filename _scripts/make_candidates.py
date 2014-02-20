import sys, os
import yaml
from slugify import slugify
from humanize.number import ordinal

party_id = sys.argv[1]

candidates = yaml.load(open("_data/{}_candidates.yaml".format(party_id)))
people = yaml.load(open("_data/{}_people.yaml".format(party_id)))
parties = yaml.load(open("_data/parties.yaml"))
regions = yaml.load(open("_data/regions.yaml"))
party = parties[party_id]

for region_id in candidates:
  region = regions[region_id]
  for i, candidate in enumerate(candidates[region_id]):
    person_id = slugify(unicode(candidate['name']))
    person = people[person_id]

    rank = i+1
    rank_ordinal = ordinal(rank)

    s = """---
layout: candidate
permalink: candidates/eu2014/{}/{}/
categories: candidate {}
election: eu2014
list-rank: {}
list-rank-ordinal: {}
person: {}
region: {}
party: {}
title: {} - {} - {}
---""".format(party_id, person_id, party_id, rank, rank_ordinal, person_id, region_id, party_id, region['name'], party['name'], candidate['name'])

    dir_path = os.path.join("_candidates", "eu2014", party_id)
    if not os.path.isdir(dir_path):
      os.mkdir(dir_path)

    path = os.path.join(dir_path, "{}.md".format(person_id))

    #print path
    #print s

    print >>open(path, "w+"), s
