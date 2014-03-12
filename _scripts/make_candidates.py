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

    incumbent = "false"
    if 'incumbent' in candidate and candidate['incumbent']:
      incumbent = "true"

    s = u"""---
layout: candidate
permalink: candidates/eu2014/{party_id}/{person_id}/
categories: candidate {party_id}
election: eu2014
list-rank: {rank}
list-rank-ordinal: {rank_ordinal}
person: {person_id}
region: {region_id}
party: {party_id}
title: {person_name} is running for MEP in {region_name} for {party_name}
incumbent: {incumbent}
---""".format(party_id=party_id,
              person_id=person_id,
              rank=rank,
              rank_ordinal=rank_ordinal,
              region_id=region_id,
              region_name=region['name'],
              party_name=party['name'],
              candidate_name=candidate['name'],
              incumbent=incumbent)

    dir_path = os.path.join("_candidates", "eu2014", party_id)
    if not os.path.isdir(dir_path):
      os.mkdir(dir_path)

    path = os.path.join(dir_path, "{}.md".format(person_id))

    #print path
    #print s

    print >>open(path, "w+"), s.encode('utf-8')

