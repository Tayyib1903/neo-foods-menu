import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build_site',ROOT/'scripts/build_site.py')
site=importlib.util.module_from_spec(spec);spec.loader.exec_module(site)

class Anchors(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and a.get('href','').startswith('#'):self.links.append(a['href'][1:])

class BuildTests(unittest.TestCase):
    def data(self,name):return json.loads((ROOT/'content'/f'{name}.json').read_text(encoding='utf-8'))
    def menus(self):return {k:self.data(k) for k in site.MENUS}
    def test_all_pages_and_anchors(self):
        pages=site.render(ROOT)
        self.assertEqual(set(pages),{'index.html',*(k+'.html' for k in site.MENUS)})
        for name,page in pages.items():
            parser=Anchors();parser.feed(page)
            self.assertEqual(len(parser.ids),len(set(parser.ids)),name)
            self.assertTrue(set(parser.links)<=set(parser.ids),name)
            self.assertNotIn('{{',page)
    def test_edits_visibility_and_escaping(self):
        menus=self.menus();product=menus['speisekarte']['sections'][0]['groups'][0]['items'][0]
        product.update(name='<script>CMS TEST</script>',price='12,34',description='Frisch & fein',allergens='A, C')
        page=site.menu_html(ROOT,'speisekarte',menus['speisekarte'],menus)
        self.assertIn('12,34 €',page);self.assertIn('&lt;script&gt;CMS TEST',page)
        self.assertIn('Frisch &amp; fein',page);self.assertIn('Allergene: A, C',page)
        product['visible']=False
        self.assertNotIn('CMS TEST',site.menu_html(ROOT,'speisekarte',menus['speisekarte'],menus))
    def test_disabled_sections_offers_moments(self):
        menus=self.menus();menus['speisekarte']['sections'][0]['visible']=False
        page=site.menu_html(ROOT,'speisekarte',menus['speisekarte'],menus)
        self.assertNotIn('id="category-1"',page)
        page=site.home_html(ROOT,menus,[],[])
        self.assertNotIn('href="#aktionen"',page);self.assertNotIn('href="#moments"',page)
    def test_multiple_offers_moments(self):
        offers=self.data('offers')['offers'];moments=self.data('moments')['moments']
        page=site.home_html(ROOT,self.menus(),offers*2,moments*2)
        parser=Anchors();parser.feed(page)
        self.assertEqual(len(parser.ids),len(set(parser.ids)))
    def test_scoop_price_shared_with_home(self):
        menus=self.menus();menus['eiskarte']['scoop_price']='3,45'
        self.assertIn('3,45 €',site.home_html(ROOT,menus,[],[]))
        self.assertIn('3,45 €',site.menu_html(ROOT,'eiskarte',menus['eiskarte'],menus))
    def test_bad_price_and_assets_fail(self):
        for value in ['5.50','-2,00','<b>5,50</b>','']:
            with self.assertRaises(ValueError):site.money(value)
        for value in ['../secrets.png','https://example.org/a.png','javascript:alert(1)','missing.png','%2e%2e/outside.png']:
            with self.assertRaises(ValueError):site.asset(ROOT,value,{'.png'})
    def test_base_path_media(self):
        self.assertEqual(site.asset(ROOT,'/neo-foods-menu/uploads/nata-poster.png',{'.png'}),'uploads/nata-poster.png')
    def test_pdf_toggle(self):
        menus=self.menus();menus['speisekarte']['pdf_visible']=False
        self.assertNotIn('PDF laden',site.menu_html(ROOT,'speisekarte',menus['speisekarte'],menus))
    def test_all_content_has_schema(self):
        cfg=json.loads((ROOT/'.pages.yml').read_text(encoding='utf-8'))
        def check(data,fields):
            defs={f['name']:f for f in fields}
            for key,value in data.items():
                self.assertIn(key,defs)
                f=defs[key]
                if f['type']=='object':
                    for item in value:check(item,f['fields'])
        for entry in cfg['content']:
            check(json.loads((ROOT/entry['path']).read_text(encoding='utf-8')),entry['fields'])

if __name__=='__main__':unittest.main()
