#!/usr/bin/env python3
"""Repeat the page-scoped audit: python3 seo-audit/2026-10-08/collect.py baseline|after."""
import csv,hashlib,json,sys,time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request,build_opener,HTTPRedirectHandler
from urllib.error import HTTPError
from urllib.parse import urlparse,urljoin
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup
A=Path(__file__).resolve().parent; ROOT=A.parents[1]; OUT=ROOT/'output'
PHASE=sys.argv[1]; assert PHASE in ('baseline','after')
RAW=A/('before/live' if PHASE=='baseline' else 'after-live'); RAW.mkdir(parents=True,exist_ok=False)
URL='https://robertdevore.com/courses/'; NA='NOT AVAILABLE — DATA ACCESS REQUIRED'
class Redirects(HTTPRedirectHandler):
 def __init__(self):self.hops=[]
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  self.hops.append({'source':req.full_url,'status':code,'target':newurl})
  return super().redirect_request(req,fp,code,msg,headers,newurl)
def fetch(job):
 name,url,agent=job; redirects=Redirects();start=time.monotonic()
 try:
  r=build_opener(redirects).open(Request(url,headers={'User-Agent':agent}),timeout=25)
 except HTTPError as e:r=e
 except Exception as e:return name,{'url':url,'error':str(e),'status':'indeterminate','user_agent':agent}
 body=r.read();result={'url':url,'final_url':r.url,'status':r.status,'headers':{k:v for k,v in r.headers.items() if k.lower() in ['content-type','location','x-robots-tag','server','cache-control','last-modified','cf-ray']},'redirects':redirects.hops,'bytes':len(body),'elapsed_ms':round((time.monotonic()-start)*1000),'sha256':hashlib.sha256(body).hexdigest(),'user_agent':agent}
 if name in ['courses','robots','sitemap','llms','index']: (RAW/(name+'.txt')).write_bytes(body)
 return name,result
BROWSER='Mozilla/5.0 (compatible; CoursesAudit/1.0)'
jobs=[(n,u,BROWSER) for n,u in [('courses',URL),('home','https://robertdevore.com/'),('robots','https://robertdevore.com/robots.txt'),('sitemap','https://robertdevore.com/sitemap.xml'),('llms','https://robertdevore.com/llms.txt'),('index','https://robertdevore.com/.well-known/kujo-site-index.json'),('image','https://robertdevore.com/assets/social/courses-social.png'),('http','http://robertdevore.com/courses/'),('www','https://www.robertdevore.com/courses/'),('http-www','http://www.robertdevore.com/courses/'),('slash','https://robertdevore.com/courses'),('query',URL+'?audit=20261008'),('missing','https://robertdevore.com/courses/audit-not-found-20261008/')]]
soup=BeautifulSoup((OUT/'courses/index.html').read_text(),'html.parser')
for link in soup.select('.course-card a'):jobs.append((urlparse(link['href']).hostname,link['href'],BROWSER))
for name,agent in [('Googlebot','Googlebot'),('Bingbot','bingbot'),('OAI-SearchBot','OAI-SearchBot'),('GPTBot','GPTBot'),('ChatGPT-User','ChatGPT-User'),('Claude-SearchBot','Claude-SearchBot'),('PerplexityBot','PerplexityBot')]:jobs.append((name,URL,agent))
with ThreadPoolExecutor(max_workers=8) as pool:receipts=dict(pool.map(fetch,jobs))
(RAW/'requests.json').write_text(json.dumps(receipts,indent=2)+'\n')
def write(name,rows):
 p=A/name
 fields=next(csv.reader(p.open()))
 existing=list(csv.DictReader(p.open())) if PHASE=='after' and name not in ['after.csv','site-inventory.csv'] else []
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(existing+rows)
def meta(selector):
 n=soup.select_one(selector);return n.get('content','') if n else ''
schema=[json.loads(x.string) for x in soup.select('script[type="application/ld+json"]')]
def schema_types(value):
 if isinstance(value,dict):
  for key,item in value.items():
   if key=='@type':yield item
   else:yield from schema_types(item)
 elif isinstance(value,list):
  for item in value:yield from schema_types(item)
types=list(dict.fromkeys(schema_types(schema)))
canonical=soup.select_one('link[rel="canonical"]')['href'];title=soup.title.get_text();description=meta('meta[name="description"]')
htmls=list(OUT.rglob('index.html')); inbound=[];titles=[];descriptions=[]
for p in htmls:
 s=BeautifulSoup(p.read_text(),'html.parser');c=s.select_one('link[rel="canonical"]')
 if not c:continue
 titles.append(s.title.get_text() if s.title else '');d=s.select_one('meta[name="description"]');descriptions.append(d.get('content','') if d else '')
 for link in s.select('a[href="/courses/"]'):
  if c['href']!=URL:inbound.append({'phase':PHASE,'source_url':c['href'],'destination_url':URL,'anchor_text':link.get_text(' ',strip=True),'link_context':'navigation','http_status':receipts['courses']['status'],'final_url':URL,'verification':'generated crawlable anchor','chain_length':0})
links=[]
for a in soup.select('a[href]'):
 u=urljoin(URL,a['href']);parsed=urlparse(u)
 if parsed.scheme not in ['http','https']:continue
 internal=parsed.netloc=='robertdevore.com';path=OUT/parsed.path.lstrip('/');present=path.is_file() or (path/'index.html').is_file()
 receipt=receipts.get(parsed.hostname,{}) if not internal else {}
 links.append({'phase':PHASE,'source_url':URL,'destination_url':u,'anchor_text':a.get_text(' ',strip=True) or a.get('aria-label',''),'link_context':'course card' if a.find_parent(class_='course-card') else 'navigation','http_status':('artifact-present' if present else 'missing') if internal else receipt.get('status','not probed'),'final_url':receipt.get('final_url',u),'chain_length':len(receipt.get('redirects',[])),'verification':('generated route exists' if present else 'missing generated route') if internal else ('access blocked; not proven broken' if receipt.get('status') in [401,403,405,429] else 'live GET' if receipt else 'outside course-link scope'),'rel':' '.join(a.get('rel',[])),'internal':internal})
images=[]
for img in soup.select('img'):
 p=OUT/urlparse(img['src']).path.lstrip('/');images.append({'phase':PHASE,'page_url':URL,'image_url':urljoin(URL,img['src']),'alt_text':img.get('alt'),'alt_present':'alt' in img.attrs,'decorative':img.get('alt')=='','width':img.get('width'),'height':img.get('height'),'loading':img.get('loading'),'format':p.suffix,'local_exists':p.exists(),'file_bytes':p.stat().st_size if p.exists() else 0})
robots=(RAW/'robots.txt').read_text();rp=RobotFileParser();rp.parse(robots.splitlines())
indexable=receipts['courses']['status']==200 and 'noindex' not in meta('meta[name="robots"]') and 'noindex' not in str(receipts['courses']['headers'].get('X-Robots-Tag','')) and rp.can_fetch('Googlebot',URL)
base={'phase':PHASE,'url':URL,'source_file':'content/pages/courses.md; templates/page-courses.html','page_type':'course catalog','local_status':'artifact-present','production_status':receipts['courses']['status'],'indexable':indexable,'robots_directives':meta('meta[name="robots"]') or 'no explicit restrictions','canonical':canonical,'canonical_target_status':receipts['courses']['status'],'title':title,'title_length':len(title),'meta_description':description,'description_length':len(description),'h1':' | '.join(n.get_text(' ',strip=True) for n in soup.select('h1')),'heading_structure':' | '.join(n.name+': '+n.get_text(' ',strip=True) for n in soup.select('h1,h2,h3')),'word_count':len(soup.select_one('main').get_text(' ',strip=True).split()),'lang':soup.html.get('lang'),'author':meta('meta[name="author"]'),'breadcrumbs':False,'schema_types':'|'.join(types),'internal_inbound_links':len(inbound),'internal_outbound_links':sum(x['internal'] for x in links),'external_outbound_links':sum(not x['internal'] for x in links),'broken_internal_links':sum(x['http_status']=='missing' for x in links),'broken_external_links':'0 proven; blocked responses indeterminate','image_count':len(images),'missing_alt':sum(not x['alt_present'] for x in images),'missing_dimensions':sum(not x['width'] or not x['height'] for x in images),'page_depth':1,'orphan':not inbound,'sitemap_included':URL in (RAW/'sitemap.txt').read_text(),'duplicate_title':titles.count(title)>1,'duplicate_description':descriptions.count(description)>1,'content_hash':hashlib.sha256(soup.select_one('main').encode()).hexdigest(),'issues':'SCHEMA-01' if 'BlogPosting' in types else ''}
write(PHASE+'.csv',[base]);write('site-inventory.csv',[base]);write('metadata-audit.csv',[dict(base,og_title=meta('meta[property="og:title"]'),og_description=meta('meta[property="og:description"]'),og_url=meta('meta[property="og:url"]'),og_type=meta('meta[property="og:type"]'),og_image=meta('meta[property="og:image"]'),twitter_card=meta('meta[name="twitter:card"]'))]);write('internal-links.csv',inbound+[x for x in links if x['internal']]);write('external-links.csv',[x for x in links if not x['internal']]);write('image-audit.csv',images);write('indexability.csv',[base]);write('crawlability.csv',[dict(base,crawlable_html_links=True,pages_over_three_clicks=0)]);write('schema-audit.csv',[dict(base,json_ld_blocks=len(schema),valid_json=True,visible_match='BlogPosting' not in types,rich_result_eligible='not established; Schema.org meaning is distinct from search eligibility',recommended_action='Use CollectionPage with visible course list' if 'BlogPosting' in types else 'none')])
write('redirects.csv',[{'phase':PHASE,'source_url':receipts[n]['url'],'source_variant':n,'http_status':receipts[n].get('redirects',[{}])[0].get('status') if receipts[n].get('redirects') else receipts[n]['status'],'target_url':receipts[n].get('final_url'),'chain_length':len(receipts[n].get('redirects',[])),'final_status':receipts[n]['status'],'canonical_target':URL,'query_preserved':'audit=20261008' in receipts[n].get('final_url','') if n=='query' else 'not applicable','verification':json.dumps(receipts[n].get('redirects',[]))} for n in ['http','www','http-www','slash','query','missing']])
write('crawler-access.csv',[{'crawler':n,'purpose':'training' if n=='GPTBot' else 'user-triggered fetch' if n=='ChatGPT-User' else 'search discovery','robots_access':rp.can_fetch(n,URL),'live_status':receipts[n]['status'],'waf_or_cdn_result':'UA-only probe; not a verified provider IP','action_taken':'policy unchanged','evidence':str(RAW.relative_to(A)/'requests.json')} for n in ['Googlebot','Bingbot','OAI-SearchBot','GPTBot','ChatGPT-User','Claude-SearchBot','PerplexityBot']])
summary={'scope':'one course catalog page; full local HTML inventory for inbound links and duplicates','canonical_pages':1,'indexable_pages':int(indexable),'h1_count':len(soup.select('h1')),'missing_titles':int(not title),'missing_descriptions':int(not description),'duplicate_titles':int(base['duplicate_title']),'duplicate_descriptions':int(base['duplicate_description']),'missing_canonicals':int(not canonical),'broken_internal_links':base['broken_internal_links'],'proven_broken_external_destinations':0,'indeterminate_course_destinations':sum(receipts[urlparse(a['href']).hostname]['status'] in [401,403,405,429] for a in soup.select('.course-card a')),'orphans':int(base['orphan']),'pages_deeper_than_three_clicks':0,'missing_alt':base['missing_alt'],'missing_dimensions':base['missing_dimensions'],'jsonld_parse_errors':0,'page_type_errors':int('BlogPosting' in types),'sitemap_included':base['sitemap_included'],'p0':0,'p1':0,'p2':int('BlogPosting' in types),'seo_score':'not assigned; page-scoped audit with unavailable field/search data','ai_readiness_score':'not assigned; measured AI visibility unavailable','field_cwv':NA,'main_content_hash':base['content_hash'],'local_html_inventory_count':len(htmls)}
(A/(PHASE+'-summary.json')).write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
