YourNextMEP
===========

Slightly silly idea of making a UK European Elections 2014 candidate site entirely in Jekyll.

The data is more or less [Popolo project](http://popoloproject.com/) compliant! It has now been uploaded to https://yournextmep.popit.mysociety.org for long term reference and easy API access.

Installing
----------

These are untested notes.

First, have Jekyll installed.

    gem install jekyll
    
Next, have python-yaml and pyaml installed

    pip install yaml pyaml

Make directories to store the Twitter images.

    mkdir images; mkdir images/twitter
    
Then for each party (nb: automate this) run
    
    python _scripts/twitter_pics.py _data/PARTYID_people.yaml
    python _scripts/wikipedia_biogs.py _data/PARTYID_people.yaml
    
to get the Twitter images and wikipedia descriptions.

If you want to rebuild the candidates pages (e.g. you've added or renamed a candidates), run

    python _scripts/make_candidates.py PARTYID
    
and the appropriate files in _candidates will be made.
    
Finally, build with Jekyll

    jekyll build
    
and you can now serve the static content out of _site with e.g. nginx.

Also, Flask API servers for postcode lookups in _api, run as uwsgi under nginx with the path prefix /api.

Finally, Flask API servers for email reminders in _reminders. Edit settings.py and run as uwsgi under nginx with the path prefix /reminder.
