import lxml.html
import sys
import requests

url = "http://dbpedia.org/data/{}.json"
index = "http://dbpedia.org/resource/{}"

wiki_url = "http://en.wikipedia.org/wiki/{}"

def get_page(wikipedia_page):
  resp = requests.get(url.format(wikipedia_page))
  return resp.json()

def get_wiki_page(wikipedia_page):
  url = wiki_url.format(wikipedia_page)
  resp = requests.get(url)
  return resp.text

def get_comment(wikipedia_page, lang='en'):
  idx = index.format(wikipedia_page)

  p = get_page(wikipedia_page)[idx]
  if 'http://www.w3.org/2000/01/rdf-schema#comment' in p:
    a = p['http://www.w3.org/2000/01/rdf-schema#comment']
    a = [x for x in a if x['lang'] == lang]
    return a[0]
  else:
    return None

def get_image(wikipedia_page, lang='en'):
  idx = index.format(wikipedia_page)

  p = get_wiki_page(wikipedia_page)

  tree = lxml.html.fromstring(p)

  img_url = tree.xpath('//td[@class="logo"]/a/img/@src')[0]
  img_source = tree.xpath('//td[@class="logo"]/a/@href')[0]

  return img_url, img_source

if __name__ == "__main__":
  #print get_comment(sys.argv[1]) 
  print get_image(sys.argv[1])
  #print get_wiki_page(sys.argv[1])

