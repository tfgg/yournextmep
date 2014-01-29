import sys
import requests

url = "http://dbpedia.org/data/{}.json"
index = "http://dbpedia.org/resource/{}"

def get_page(wikipedia_page):
  resp = requests.get(url.format(wikipedia_page))
  return resp.json()

def get_comment(wikipedia_page, lang='en'):
  idx = index.format(wikipedia_page)

  p = get_page(wikipedia_page)[idx]
  if 'http://www.w3.org/2000/01/rdf-schema#comment' in p:
    a = p['http://www.w3.org/2000/01/rdf-schema#comment']
    a = [x for x in a if x['lang'] == lang]
    return a[0]
  else:
    return None

if __name__ == "__main__":
  print get_comment(sys.argv[1]) 
