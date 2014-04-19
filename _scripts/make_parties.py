import sys, os
import yaml
from slugify import slugify
from humanize.number import ordinal

parties = yaml.load(open("_data/parties.yaml"))

for party_id, party in parties.items():
  s = u"""---
layout: party
permalink: parties/{party_id}/
categories: party {party_id}
party: {party_id}
title: {party_name} in the European Parliament
---""".format(party_id=party_id,
              party_name=party['name'])

  out_path = os.path.join("_parties/", "{}.md".format(party_id))

  print >>open(out_path, "w+"), s.encode('utf-8')

