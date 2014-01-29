import sys
import yaml

party = sys.argv[2]
region = sys.argv[2]
person_id = sys.argv[3]
rank = int(sys.argv[4])

s = """---
layout: candidate
categories: candidate labour
election: eu2014
list-rank: {}
person: {}
region: {}
party: {}
---""".format(rank, person_id, region, party)

print >>open("{}.md".format(person_id), "w+"), s
