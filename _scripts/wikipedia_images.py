import os
import requests
import sys
from grab_dbpedia import get_comment, get_image
import yaml, pyaml

people = yaml.load(open(sys.argv[1]))

def get_wikipedia_id(wikipedia_url):
  return wikipedia_url.split('/')[-1]

content_types = {'image/jpeg': 'jpg',
                 'image/png': 'png',
                 'image/gif': 'gif',}

target_dir = "images/wikipedia"

for person_id in people:
  person = people[person_id]

  if 'image' in person:
    continue

  if 'links' in person:
    for link in person['links']:
      if 'wikipedia' in link['url']:
        wikipedia_id = get_wikipedia_id(link['url'])

        try:
          img_url, img_source = get_image(wikipedia_id)

          if img_url is not None:
            resp = requests.get("http:" + img_url, stream=True)
            ext = content_types[resp.headers['content-type']]
      
            path = os.path.join(target_dir, "{}.{}".format(person['id'], ext))

            with open(path, 'wb') as f:
              for chunk in resp.iter_content():
                f.write(chunk)

            person['image'] = "/" + path
            person['image_source'] = "http://en.wikipedia.org" + str(img_source)

        except Exception, e:
          print e

#pyaml.dump(people, sys.stdout, vspacing=[2,0])

f = open(sys.argv[1], 'w+')
pyaml.dump(people, f, vspacing=[2,0])
f.close()

