import requests
import sys
import os
import yaml
import pyaml
import twitter

def get_twitter_id(twitter_url):
  return twitter_url.split('/')[-1]

def get_twitter_missing(people, fresh=False):
  ids = []
  for person_id, person in people.items():
    if 'links' in person:
      for link in person['links']:
        if 'twitter' in link['url']:
          twitter_id = get_twitter_id(link['url'])

          if twitter_id == "":
            print >>sys.stderr, link, person_id

          if 'image' not in person or fresh:
            #not os.path.isfile(os.path.join('.', person['image'])):
            ids.append((person, twitter_id))

  return ids

def get_twitter_images(api, ids, target_dir="images/twitter"):
  for person, twitter_id in ids:
    print >>sys.stderr, twitter_id

    try:
      user = api.GetUser(screen_name=twitter_id)
    except twitter.TwitterError, e:
      print "Twitter error:", e
      continue

    profile_image_url = user.profile_image_url
    description = user.description

    profile_image_url = profile_image_url.replace("_normal", "")

    resp = requests.get(profile_image_url, stream=True)

    if resp.status_code == 200:
      ext = content_types[resp.headers['content-type']]

      path = os.path.join(target_dir, "{}.{}".format(twitter_id, ext))

      with open(path, 'wb') as f:
        for chunk in resp.iter_content():
          f.write(chunk)

      if 'image' not in person or not person['image'].startswith('/images/other'):
        person['image'] = "/" + path

      person['summary'] = description

def write_people(people, target):
  f = open(target, 'w+')
  pyaml.dump(people, f, vspacing=[2, 0])
  f.close()

if __name__ == "__main__":
  from local_settings import TWITTER
  import twitter

  api = twitter.Api(consumer_key=TWITTER['consumer_key'],
                    consumer_secret=TWITTER['consumer_secret'],
                    access_token_key=TWITTER['access_token_key'],
                    access_token_secret=TWITTER['access_token_secret'])

  content_types = {'image/jpeg': 'jpg',
                   'image/png': 'png',
                   'image/gif': 'gif',}

  for people_path in sys.argv[1:]:
    print ">", people_path
    people = yaml.load(open(people_path))
    ids = get_twitter_missing(people, True)
    get_twitter_images(api, ids)
    write_people(people, people_path)

