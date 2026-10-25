const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const file=path.join(__dirname,'../review/02-ia-v8.html');assert.ok(fs.existsSync(file),'v8 required');
const html=fs.readFileSync(file,'utf8');const js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
class E {
 constructor(tag){this.tagName=tag;this.children=[];this.attrs={};this.textContent='';this.scrollTop=0;}
 append(...n){this.children.push(...n);} replaceChildren(...n){this.children=n;}
 setAttribute(k,v){this.attrs[k]=v;} focus(){this.focused=true;}
 querySelector(selector){return walk(this).find(x=>selector.includes(x.attrs['data-prayer-mode'])&&x.attrs['data-prayer-mode']);}
}
function walk(n){return [n,...n.children.flatMap(walk)];}
const nav=new E('nav');nav.parentElement={scrollTop:45};
const sb={document:{createElement:t=>new E(t),createElementNS:(_,t)=>new E(t),querySelector:()=>nav}};
vm.createContext(sb);vm.runInContext(js.slice(0,js.indexOf("find('part-prev').onclick")),sb);
const run=c=>vm.runInContext(c,sb);
run("selectedItem=contents[1][7].id;renderToc()");
const links=walk(nav).filter(x=>x.tagName==='a');assert.equal(links.length,26);
assert.equal(links.filter(x=>x.attrs['aria-current']==='location').length,1);
assert.equal(links.find(x=>x.attrs['aria-current']).textContent,'보편 지향 기도');
assert.equal(nav.parentElement.scrollTop,45);
assert.ok(html.includes('<aside class="reader__rail"'));
assert.equal(html.includes('data-panel="toc"'),false);
assert.equal(js.includes("if (which === 'toc')"),false);
const card=run("renderPrayerCard('자비송','자비송')");
let buttons=walk(card).filter(x=>x.tagName==='button');assert.equal(buttons.length,2);
assert.equal(buttons[0].attrs['aria-pressed'],'true');assert.equal(walk(card).some(x=>x.tagName==='select'),false);
buttons[1].onclick();buttons=walk(card).filter(x=>x.tagName==='button');
assert.equal(buttons[1].attrs['aria-pressed'],'true');assert.equal(buttons[0].attrs['aria-pressed'],'false');
assert.equal(walk(card).filter(x=>x.tagName==='figure').length,1);assert.equal(buttons[1].focused,true);
buttons[0].onclick();assert.equal(walk(card).filter(x=>x.tagName==='figure').length,0);
assert.equal(run("frameSpecs['입당 성가'].source"),'hymnSet');
console.log('PASS: 26 rail links, current marker, rail scroll, no TOC dialog trigger; two toggle buttons, pressed state, score display, focus, hymn scope');
