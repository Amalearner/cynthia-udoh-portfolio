"""Render the approved portfolio design with editor-managed content. No dependencies."""
from pathlib import Path
import os,json,re,html,shutil,urllib.parse
ROOT=Path(__file__).parent
ORIGIN=os.environ.get('PAGES_BASE_URL','https://amalearner.github.io/cynthia-udoh-portfolio').rstrip('/')
OUT=ROOT/'_site'

def read(path):return json.loads((ROOT/path).read_text())
def escape(s):return html.escape(str(s),quote=True)
def safe_link(value):
 value=str(value).strip()
 if urllib.parse.urlsplit(value).scheme.lower() not in ('','http','https','mailto','tel'):raise ValueError('Unsupported link protocol')
 if value.startswith('/assets/'):value='.'+value
 return value

def resolve(data,key):
 for part in key.split('.'):data=data[part]
 return data

def fill(template,data):
 def replace(match):
  path=match[1];value=resolve(data,path)
  if '.link_' in path or '.image_src_' in path:value=safe_link(value)
  return escape(value)
 return re.sub(r'\{\{((?:global|page)\.[a-zA-Z0-9_.]+)\}\}',replace,template)

def build():
 OUT.mkdir(exist_ok=True)
 # Only generated output is replaced; source and editable content are untouched.
 for f in OUT.iterdir():
  if f.is_dir():shutil.rmtree(f)
  else:f.unlink()
 templates=read('templates.json');settings=read('content/settings.json')
 globals={tag:fill(templates['global_'+tag],{'global':settings}) for tag in ['header','footer']}
 pages=[]
 for path in sorted((ROOT/'content/pages').glob('*.json')):
  page=json.loads(path.read_text());name=path.stem+'.html';template=templates[name]
  def section(m):return m[2] if page[m[1]].get('visible',True) else ''
  template=re.sub(r'<!--CMS:START:(section_\d+)-->(.*?)<!--CMS:END:\1-->',section,template,flags=re.S)
  template=template.replace('{{GLOBAL_HEADER}}',globals['header']).replace('{{GLOBAL_FOOTER}}',globals['footer'])
  result=fill(template,{'global':settings,'page':page})
  pageURL=ORIGIN+('/' if name=='index.html' else '/'+name)
  result=result.replace('https://amalearner.github.io/cynthia-udoh-portfolio',ORIGIN)
  def ld(m):
   data=json.loads(m[1]);data.update(name=page['title'],description=page['description'],url=pageURL)
   return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+'</script>'
  result=re.sub(r'<script type="application/ld\+json">(.*?)</script>',ld,result,flags=re.S)
  assert '{{' not in result,('Unresolved content token',name)
  (OUT/name).write_text(result);pages.append(pageURL)
 for path in ROOT.iterdir():
  if path.suffix in ['.css','.js']:shutil.copy2(path,OUT/path.name)
 shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
 interactions=read('content/interactions.json')
 if len(interactions['stages'])!=4:raise ValueError('Keep four delivery stages; edit their copy rather than changing their number.')
 if not interactions['rings']:raise ValueError('Keep at least one ring note.')
 def js_string(s):return escape(s).replace('\n','<br>')
 stages=[[js_string(x[k]) for k in ['symbol','title','description','output']] for x in interactions['stages']]
 app=(OUT/'app.js').read_text();app=re.sub(r'const stages=\[.*?\];',lambda m:'const stages='+json.dumps(stages)+';',app,flags=re.S);(OUT/'app.js').write_text(app)
 rings=[[x['label'],x['text']] for x in interactions['rings']]
 script=(OUT/'ring.js').read_text();script=re.sub(r'const ringThoughts=\[.*?\];',lambda m:'const ringThoughts='+json.dumps(rings)+';',script,flags=re.S);(OUT/'ring.js').write_text(script)
 decks=[]
 for item in interactions['decks']:
  if not item['slides']:raise ValueError('Each notebook needs at least one sketch.')
  deck={k:item[k] for k in ['title','label']};deck['slides']=[]
  for itemSlide in item['slides']:
   slide={k:js_string(itemSlide.get(k,'')) for k in ['tag','title','note','footer']}
   if itemSlide.get('cards'):slide['cards']=[[js_string(c['label']),js_string(c['text'])] for c in itemSlide['cards']]
   else:slide['steps']=[js_string(x['text']) for x in itemSlide.get('steps',[])]
   deck['slides'].append(slide)
  decks.append(deck)
 sketch=(OUT/'sketches.js').read_text();sketch='const decks='+json.dumps(decks,ensure_ascii=False)+';\n'+sketch[sketch.index('const dialog='):]
 sketch=sketch.replace("slideIndex<4","slideIndex<decks[deckIndex].slides.length-1").replace("+' of 5'","+' of '+deck.slides.length")
 # Existing notebook cover buttons stay connected to their edited content.
 sketch+='\ndocument.querySelectorAll("[data-deck]").forEach(b=>{const d=decks[Number(b.dataset.deck)];if(!d){b.hidden=true;return;}b.querySelector("h2").textContent=d.title;b.querySelector(".deck-kicker").textContent=d.label;const c=b.querySelector(".cover-bottom");if(c?.firstChild)c.firstChild.textContent=d.slides.length+" SKETCHES ";});\n'
 (OUT/'sketches.js').write_text(sketch)
 (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(x)+'</loc></url>' for x in pages)+'</urlset>')
 (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
 (OUT/'.nojekyll').write_text('')
 (OUT/'admin').mkdir(exist_ok=True)
 (OUT/'admin/index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Edit your portfolio</title><style>body{background:#fbf6ee;color:#171717;font:22px/1.6 system-ui;max-width:700px;margin:12vh auto;padding:28px}a{color:#2348e6}</style><h1>Your portfolio editor</h1><p>Edit a page, upload an image, or update your social links in Pages CMS. Save your changes to publish them automatically.</p><p><a href="https://app.pagescms.org/">Open the content editor ↗</a></p><p>Sign in with GitHub, then choose <strong>Amalearner / cynthia-udoh-portfolio</strong> and the <strong>main</strong> branch.</p><p><a href="../">Back to your portfolio</a></p></html>')
 print('Built',len(pages),'editable pages for',ORIGIN)
if __name__=='__main__':build()
