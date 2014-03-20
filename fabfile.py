import os
from fabric.api import env, run, cd, local

env.hosts = ['yournextmep@yournextmep.com']

def deploy():
  push()
  pull()
  build()

def party_ids():
  with cd('~/site/'):
    for f in os.listdir('_data'): 
      if f.endswith('_people.yaml'):
        yield f[:-len("_people.yaml")]

def twitter_images(party=None):
  if party is None:
    print "Doing all"
  else:
    print "Doing", party

def wikipedia_biogs(party=None):
  pass

def push():
  local('git push origin master')

def pull():
  with cd('~/site/'):
    run('git pull gh master')

def build():
  with cd('~/site/'):
    run('jekyll build')

def stop_api():
  pass

def run_api():
  with cd('~/site/_api'):
    run('bash run')

