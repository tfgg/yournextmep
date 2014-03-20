import os
from fabric.api import env, run, cd, local

env.hosts = ['yournextmep@yournextmep.com']

def deploy():
  push()
  pull()
  build()

def twitter_images():
  with cd('~/site/'):
    for f in os.listdir('_data'): 
      if f.endswith('_people.yaml'):
        print f

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

