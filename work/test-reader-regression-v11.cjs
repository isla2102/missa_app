const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const root=path.join(__dirname,'..');const file=path.join(root,'review/02-ia-v11.html');assert.ok(fs.existsSync(file),'v9 review required');
const html=fs.readFileSync(file,'utf8');assert.ok(html.includes('<option value="main" selected>교중미사</option>'));
const js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const walk=n=>[n,...n.children.flatMap(walk)];
class E{
 constructor(tag){this.tagName=tag;this.children=[];this.attrs={};this.textContent='';}
 append(...nodes){this.children.push(...nodes);}replaceChildren(...nodes){this.children=nodes;}
 setAttribute(k,v){this.attrs[k]=v;}addEventListener(){}focus(){this.focused=true;}
 closest(){return null;} querySelector(selector){const mode=selector.match(/data-prayer-mode="(.*?)"/);return walk(this).find(x=>mode?x.attrs['data-prayer-mode']===mode[1]:x.tagName===selector);}
}
const slot={value:'main',selectedOptions:[{textContent:'교중미사'}]};
const sandbox={document:{createElement:t=>new E(t),createElementNS:(_,t)=>new E(t),querySelector:()=>slot}};
vm.createContext(sandbox);vm.runInContext(js.slice(0,js.indexOf("find('part-prev').onclick")),sandbox);
const run=c=>vm.runInContext(c,sandbox);
const frame=run("renderPrayerFrame('자비송','자비송')");
assert.equal(frame.children[0].className,'reader__item-heading');
assert.equal(frame.children[0].children[0].tagName,'h3');
assert.equal(walk(frame.children[0]).filter(x=>x.tagName==='button').length,2);
const card=frame.children[1];assert.equal(walk(card).some(x=>x.tagName==='button'),false);
assert.equal(walk(card).filter(x=>x.tagName==='image').length,1);
assert.equal(walk(frame.children[0]).find(x=>x.attrs['data-prayer-mode']==='chant').attrs['aria-pressed'],'true');
walk(frame.children[0]).find(x=>x.attrs['data-prayer-mode']==='recite').onclick();assert.equal(walk(card).some(x=>x.tagName==='image'),false);
walk(frame.children[0]).find(x=>x.attrs['data-prayer-mode']==='chant').onclick();assert.equal(walk(card).filter(x=>x.tagName==='image').length,1);
assert.equal(run("scoreAssets('대영광송').length"),2);assert.equal(run("scoreAssets('주님의 기도').length"),2);
assert.equal(run("scoreAssets('신앙 고백').length"),0);
const common=run('JSON.stringify(contents)');slot.value='youth';slot.selectedOptions[0].textContent='주일 저녁 젊은이 미사';
assert.equal(run("scoreAssets('자비송').length"),0);assert.equal(run('JSON.stringify(contents)'),common);
slot.value='dawn';assert.equal(run("scoreAssets('주님의 기도').length"),0);slot.value='main';
const manifest=JSON.parse(fs.readFileSync(path.join(root,'docs/교중미사악보/temporary-score-manifest.json'),'utf8'));
assert.equal(manifest.files.length,8);
const used=new Set();for(const list of Object.values(manifest.mapping))for(const asset of list){const p=path.resolve(root,'review',asset.path);assert.ok(fs.existsSync(p));used.add(path.basename(p));}
assert.equal(used.size,8);
for(const item of manifest.files){const hash=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'docs/교중미사악보',item.file))).digest('hex');assert.equal(hash,item.sha256);}
assert.ok(frame.className.includes('reader__item--score'));
console.log('PASS: default principal, title-adjacent toggle controls, photo/recitation switching, 8 file mappings+hashes, main-only score scope, common content invariant, corresponding nested cards');
