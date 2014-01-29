YourNextMEP
===========

Slightly silly idea of making a UK European Elections 2014 candidate site entirely in Jekyll.

The data might even be Popolo project compliant!

Installing
----------

These are untested notes.

First, have Jekyll installed.

    gem install jekyll
    
Next, have python-yaml and pyaml installed

    pip install yaml pyaml
    
Get the Twitter images. You can pipe the output into a new people.yaml if you want to also update the Twitter-derived descriptions.

    mkdir images; mkdir images/twitter
    python _scripts/twitter_pics.py _data/people.yaml
    
Finally, build with Jekyll

    jekyll build
    
and you can now serve the static content out of _site
