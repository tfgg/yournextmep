import requests
import re
from slugify import slugify
from flask import Flask, jsonify, request, abort

app = Flask("yournextmep-api")

region_url = "/regions/{}"

def clean_postcode(postcode):
  return re.sub('[^A-Z0-9]', '', postcode.upper())

@app.route('/api/postcode', methods=['POST'])
def postcode():
  postcode = request.form.get('postcode', None)

  if not postcode:
    return abort(500, "Specify a postcode")

  postcode = clean_postcode(postcode)

  url = "http://mapit.mysociety.org/postcode/{}".format(postcode)
  resp = requests.get(url)
  data = resp.json()

  for _, area in data['areas'].items():
    if area['type'] == 'EUR':
      return jsonify({'name': area['name'],
                      'id': slugify(area['name']),
                      'url': region_url.format(slugify(area['name']))})

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=7777)

