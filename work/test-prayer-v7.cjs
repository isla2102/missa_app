const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const path=require('node:path');
const file=path.join(__dirname,'../review/02-ia-v7.html');
assert.ok(fs.existsSync(file),'v7 must exist');
class Element {
 constructor(tag){this.tagName=tag;this.children=[];this.attrs={};this.textContent='';}
 append(...nodes){this.children.push(...nodes);}
 replaceChildren(...nodes){this.children=nodes;}
 setAttribute(k,v){this.attrs[k]=v;}
}
const js=fs.readFileSync(file,'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];
const sandbox={document:{createElement:t=>new Element(t),createElementNS:(_,t)=>new Element(t),querySelector:()=>({value:'beginner'})}};
vm.createContext(sandbox);vm.runInContext(js.slice(0,js.indexOf("find('part-prev').onclick")),sandbox);
const run=s=>vm.runInContext(s,sandbox);
assert.equal(run("frameSpecs['주님의 기도'].kind"),'prayer');
assert.equal(run("frameSpecs['입당 성가'].source"),'hymnSet');
assert.equal(run('prayerSourceRefs.scoreRef'),null);
const spoken=run("renderPrayerCard('주님의 기도','주님의 기도')");
assert.equal(spoken.children.some(x=>x.tagName==='figure'),false);
run("parishPrayerPresentation['주님의 기도']='chant'");
const sung=run("renderPrayerCard('주님의 기도','주님의 기도')");
const figure=sung.children.find(x=>x.tagName==='figure');assert.ok(figure);
assert.equal(figure.children.find(x=>x.tagName==='svg').children.length,5);
assert.ok(figure.children[0].textContent.includes('실제 악보 아님'));
assert.equal(run('contents.flat().every(item=>Boolean(frameSpecs[item.title]))'),true);
assert.equal(run("frameSpecs['성호경'].scoreSlot"),false);
assert.equal(run("Object.keys(parishPrayerPresentation).includes('dawn')"),false);
console.log('PASS: spoken/score rendering, empty source reference, five-line mock, 26 frames, shared parish scope, separate HymnSet');
