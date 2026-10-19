import json,hashlib,sys
from pathlib import Path
from bs4 import BeautifulSoup
p=Path(sys.argv[1]); s=BeautifulSoup(p.read_text(),'html.parser')
graph=[n for t in s.select('script[type="application/ld+json"]') for n in json.loads(t.string or '{}').get('@graph',[])]
c=next(n for n in graph if n.get('@type')=='CollectionPage')
cards=s.select('.course-card'); items=c['mainEntity']['itemListElement']
assert len(cards)==len(items)==c['mainEntity']['numberOfItems']
for card,item in zip(cards,items):
 assert card.h3.get_text(strip=True)==item['item']['name']
 assert card.select_one('.sk-card__actions a')['href']==item['item']['url']
 assert card.select_one('.course-card__description').get_text(' ',strip=True)==item['item']['description']
assert len(s.select('h1'))==1
assert s.select_one('link[rel="canonical"]')['href']=='https://robertdevore.com/courses/'
result={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'course_count':len(cards),'courses':[x.h3.get_text(strip=True) for x in cards],'title':s.title.get_text(),'description':s.select_one('meta[name="description"]')['content'],'canonical':s.select_one('link[rel="canonical"]')['href'],'h1_count':len(s.select('h1')),'schema_matches':True,'social_image':s.select_one('meta[property="og:image"]')['content']}
print(json.dumps(result,indent=2))
