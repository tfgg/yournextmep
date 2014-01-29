import requests
import sys
import os
import yaml
import pyaml

people = yaml.load(open(sys.argv[1]))

def get_twitter_id(twitter_url):
  return twitter_url.split('/')[-1]

ids = []
for person_id, person in people.items():
  if 'links' in person:
    for link in person['links']:
      if 'twitter' in link['url']:
        twitter_id = get_twitter_id(link['url'])
        if twitter_id == "":
          print >>sys.stderr, link, person_id

        ids.append((person, twitter_id))

from local_settings import TWITTER
import twitter

api = twitter.Api(consumer_key=TWITTER['consumer_key'],
                  consumer_secret=TWITTER['consumer_secret'],
                  access_token_key=TWITTER['access_token_key'],
                  access_token_secret=TWITTER['access_token_secret'])

content_types = {'image/jpeg': 'jpg',
                 'image/png': 'png',}

#existing = set()
#for f in os.listdir('images/twitter'):
#  existing.add(f.split('.')[0])

for person, twitter_id in ids:
  print >>sys.stderr, twitter_id

  #if twitter_id not in existing:
  user = api.GetUser(screen_name=twitter_id)
  profile_image_url = user.profile_image_url
  description = user.description

  profile_image_url = profile_image_url.replace("_normal", "")

  resp = requests.get(profile_image_url, stream=True)

  if resp.status_code == 200:
    ext = content_types[resp.headers['content-type']]

    path = "images/twitter/{}.{}".format(twitter_id, ext)

    with open(path, 'wb') as f:
      for chunk in resp.iter_content():
        f.write(chunk)

    person['image'] = "/" + path
    person['summary'] = description

pyaml.dump(people, sys.stdout, vspacing=[2, 0])

