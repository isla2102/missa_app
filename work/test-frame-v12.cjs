const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const html=fs.readFileSync('review/02-ia-v12.html','utf8'),js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const walk=n=>[n,...n.children.flatMap(walk)];
class E{constructor(t){this.tagName=t;this.children=[];this.attrs={};this.textContent='';}append(...n){this.children.push(...n)}replaceChildren(...n){this.children=n}insertBefore(n,b){this.children.splice(this.children.indexOf(b),0,n)}setAttribute(k,v){this.attrs[k]=v}getAttribute(k){return this.attrs[k]}addEventListener(){}closest(){return null}focus(){}querySelector(s){const mode=s.match(/data-prayer-mode="(.*?)"/);return walk(this).find(x=>mode?x.attrs['data-prayer-mode']===mode[1]:s[0]==='.'?x.className?.split(' ').includes(s.slice(1)):x.tagName===s)}}
const slot={value:'main',selectedOptions:[{textContent:'교중미사'}]},mode={value:'beginner'};
const sandbox={document:{createElement:t=>new E(t),createElementNS:(_,t)=>new E(t),querySelector:s=>s.includes('mode')?mode:slot}};vm.createContext(sandbox);vm.runInContext(js.slice(0,js.indexOf("find('part-prev').onclick")),sandbox);const run=c=>vm.runInContext(c,sandbox);
assert.equal(run("variantCards('인사').length"),3);assert.equal(run("variantCards('참회 예식').length"),2);
assert.equal(run("variantCards('참회 예식')[1].text.includes('+ 진심으로')"),false);
assert.ok(run("kyrieView='invocations';kyrieText()").includes('+ 진심으로'));run("kyrieView='ordinary'");
for(let i=0;i<4;i++){const blocks=run(`flowBlocks(${i})`);assert.equal(blocks.at(-1).transition,i+1);for(const b of blocks)assert.ok(run('renderBlock')(b));}
const creed=run('renderCreed()'),cards=walk(creed).filter(x=>x.attrs['data-variant']);assert.equal(cards.length,2);assert.equal(cards.filter(x=>!x.hidden).length,1);const buttons=walk(creed).filter(x=>x.attrs['data-creed-view']);buttons[1].onclick();assert.equal(cards[1].hidden,false);assert.equal(cards[0].hidden,true);assert.ok(cards.every(c=>walk(c).some(n=>n.className==='reader__text-scroll')));assert.ok(run('creedVariants().every(v=>v.text.length>200)'));
assert.equal(run("scoreAssets('대영광송').length"),4);const gloria=run("renderPrayerFrame('대영광송','대영광송')");assert.ok(gloria.className.includes('guided-score'));assert.ok(walk(gloria).some(x=>x.textContent.includes('대림과 사순')));
for(const name of ['제1독서','제2독서','복음','보편 지향 기도']){const n=run(`renderItem(contents.flat().find(x=>x.title==='${name}'))`);assert.ok(walk(n).some(x=>x.attrs['data-content-source']==='cbck-daily-mock'));assert.ok(walk(n).some(x=>x.textContent.includes('mock')))}
const ps=run("renderItem(contents.flat().find(x=>x.title==='화답송'))");assert.ok(walk(ps).some(x=>x.attrs['data-content-source']==='parish-bulletin-score'));
const collect=run("renderItem(contents.flat().find(x=>x.title==='본기도'))");assert.ok(walk(collect).some(x=>x.textContent.includes('사제가 바치는')));
const response=run("renderPrayerFrame('보편 지향 기도 응답','보편 지향 기도 응답')");assert.equal(walk(response).filter(x=>x.attrs['data-prayer-mode']).length,2);
assert.ok(html.includes('.reader__item--score.reader__item--guided-score'));
console.log('PASS: 16 comments — choice cards, no duplicate invocations, all flow blocks render, creed switching/scroll, four score pages, Gloria guide, mock readings/Gospel/intercessions, bulletin slot, collect guide, separate sung response, transitions. Browser geometry not tested.');
