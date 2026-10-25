from pathlib import Path
import re,json
root=Path('review/source');root.mkdir(parents=True,exist_ok=True);Path('tools').mkdir(exist_ok=True);Path('tests').mkdir(exist_ok=True)
s=Path('review/02-ia-v53.html').read_text(encoding='utf-8');css=re.search(r'<style>([\s\S]*?)</style>',s)[1];js=re.search(r'<script>([\s\S]*?)</script>',s)[1];shell=s.replace('<style>'+css+'</style>','<style>{{READER_CSS}}</style>').replace('<script>'+js+'</script>','<script>{{READER_JS}}</script>')
map={'dailyDocuments':'data/days/2026-10-18.json','dailySources':'data/sources.json','dailyMissaSnapshot':'docs/references/daily-missa-20261018.json','reengravedPrincipalScores':'docs/교중미사악보/reengraved/registry.json','scorePreviewSizes':'review/source/score-preview-sizes.json'}
for name,path in map.items():
 pattern=r'const '+name+r'\s*=\s*(.*?);\n';match=re.search(pattern,js);assert match,name;value=json.loads(match[1])
 if name=='scorePreviewSizes':Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
 elif name=='dailyDocuments':assert value==[json.loads(Path(path).read_text(encoding='utf-8'))]
 else:assert value==json.loads(Path(path).read_text(encoding='utf-8')),name
 js=re.sub(pattern,lambda _:f'const {name} = {{{{{name}}}}};\n',js,count=1)
for name,text in [('shell.html',shell),('reader.css',css),('reader.js',js)]: (root/name).write_text(text,encoding='utf-8',newline='\r\n')
config={'baseline':'review/02-ia-v53.html','output':'review/02-ia-current.html','bindings':{name:{'path':path,'array':name=='dailyDocuments'} for name,path in map.items()}}
(root/'build.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf-8')
t=Path('work/test-reader-v53.cjs').read_text(encoding='utf-8').replace("fs.readFileSync('review/02-ia-v53.html','utf8')","fs.readFileSync(process.env.MISSA_REVIEW_FILE||'review/02-ia-current.html','utf8')")
Path('tests/reader-regression.cjs').write_text(t,encoding='utf-8',newline='\r\n')
print('Extracted baseline into source files; all external data matches embedded v53 values.')
