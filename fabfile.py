from fabric.api import env, run, cd, local

env.hosts = ['yournextmep.com']

def deploy():
  push()
  pull()
  build()

def push():
  local('git push')

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

