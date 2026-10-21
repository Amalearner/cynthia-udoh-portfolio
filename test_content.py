import unittest,tempfile,shutil,json,importlib.util
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).parent
class References(HTMLParser):
 def __init__(self):super().__init__();self.paths=[];self.h1=0
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag=='h1':self.h1+=1
  for key in ['href','src']:
   value=attrs.get(key,'')
   if value.startswith('./'):self.paths.append(value.split('#')[0])
class ContentEditing(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();cls.root=Path(cls.temp.name)
  shutil.copytree(ROOT,cls.root,dirs_exist_ok=True,ignore=shutil.ignore_patterns('_site','.git'))
  spec=importlib.util.spec_from_file_location('sitebuilder',cls.root/'build-pages.py');cls.builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.builder);cls.builder.ROOT=cls.root;cls.builder.OUT=cls.root/'_site'
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def test_edit_text_hide_section_and_update_interactions(self):
  path=self.root/'content/pages/index.json';data=json.loads(path.read_text());first=data['section_01'];key=next(k for k,v in first.items() if isinstance(v,str) and 'Your ambition.' in v);first[key]='Your next great launch.';data['section_02']['visible']=False;path.write_text(json.dumps(data))
  settings=self.root/'content/settings.json';globalData=json.loads(settings.read_text());key=next(k for k,v in globalData['footer'].items() if v=='https://x.com/thecynthiaudoh');globalData['footer'][key]='https://x.com/example';settings.write_text(json.dumps(globalData))
  interactions=self.root/'content/interactions.json';notes=json.loads(interactions.read_text());notes['rings'][0]['text']='Align the team before the launch.';notes['decks'][0]['slides'][0]['note']='Start with a shared outcome.';interactions.write_text(json.dumps(notes))
  self.builder.build();out=self.root/'_site';home=(out/'index.html').read_text()
  self.assertIn('Your next great launch.',home);self.assertNotIn('CLARITY IS A CREATIVE ADVANTAGE',home);self.assertIn('https://x.com/example',home)
  self.assertIn('Align the team before the launch.',(out/'ring.js').read_text());self.assertIn('Start with a shared outcome.',(out/'sketches.js').read_text())
  for page in out.glob('*.html'):
   parser=References();parser.feed(page.read_text());self.assertEqual(parser.h1,1,page.name)
   for path in parser.paths:self.assertTrue((out/path).exists(),(page.name,path))
if __name__=='__main__':unittest.main()
