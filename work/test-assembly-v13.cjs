const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const html=fs.readFileSync('review/02-ia-v13.html','utf8'),js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const walk=n=>[n,...n.children.flatMap(walk)];
class E{
 constructor(t){this.tagName=t;this.children=[];this.attrs={};this._text='';this.className='';this.classList={contains:c=>this.className.split(' ').includes(c),add:c=>{if(!this.classList.contains(c))this.className+=' '+c}};}
 get textContent(){return this._text+this.children.map(n=>n.textContent).join('')}set textContent(t){this._text=t;this.children=[]}
 append(...n){n.forEach(x=>x.parentElement=this);this.children.push(...n)}replaceChildren(...n){this._text='';this.children=[];this.append(...n)}
 replaceWith(n){const p=this.parentElement;if(p){p.children.splice(p.children.indexOf(this),1,n);n.parentElement=p;}}
 insertBefore(n,b){n.parentElement=this;this.children.splice(this.children.indexOf(b),0,n)}setAttribute(k,v){this.attrs[k]=v}getAttribute(k){return this.attrs[k]}addEventListener(){}closest(){return null}focus(){}
 querySelectorAll(s){return walk(this).slice(1).filter(x=>s[0]==='.'?x.classList.contains(s.slice(1)):x.tagName===s)}querySelector(s){return this.querySelectorAll(s)[0]}
}
const slot={value:'main',selectedOptions:[{textContent:'교중미사'}]},mode={value:'beginner'};
const sandbox={document:{createElement:t=>new E(t),createElementNS:(_,t)=>new E(t),querySelector:s=>s.includes('mode')?mode:slot}};vm.createContext(sandbox);vm.runInContext(js.slice(0,js.indexOf("find('part-prev').onclick")),sandbox);const run=c=>vm.runInContext(c,sandbox);
const roles=n=>walk(n).filter(x=>x.attrs['data-speech-role']);
const sign=run("renderBlock(flowBlocks(0).find(b=>b.item?.title==='성호경'))");assert.equal(roles(sign).filter(x=>x.attrs['data-speech-role']==='assembly').length,1);assert.ok(roles(sign).find(x=>x.attrs['data-speech-role']==='assembly').textContent.includes('◎ 아멘.'));
const greetings=run("flowBlocks(0).filter(b=>b.group==='인사')");assert.equal(greetings.length,3);assert.ok(greetings.every(b=>!b.variant.text.includes('◎')));
const common=run("flowBlocks(0).filter(b=>b.group==='인사 합송')");assert.equal(common.length,1);assert.equal(common[0].variant.text,'◎ 또한 사제의 영과 함께.');
const conf=run("renderBlock(flowBlocks(0).find(b=>b.group==='참회 예식'))");const assembly=roles(conf).filter(x=>x.attrs['data-speech-role']==='assembly');assert.equal(assembly.length,2);assert.ok(assembly[0].textContent.includes('형제들에게'));assert.ok(assembly[0].textContent.includes('제 탓이요'));assert.ok(assembly[0].textContent.includes('빌어 주소서'));assert.ok(assembly[0].querySelector('.reader__guidance'));assert.ok(assembly[1].textContent.includes('아멘'));
assert.ok(roles(conf).find(x=>x.attrs['data-speech-role']==='priest').textContent.includes('형제 여러분'));
// Every marked response in each reference is assigned to an assembly segment, including continuation lines.
for(const record of run('localOrdinaryReference.records')){const segments=run('spokenSegments')(record.text);const markers=record.text.split('\n').filter(l=>l.trim().startsWith('◎'));for(const line of markers)assert.ok(segments.some(s=>s.kind==='assembly'&&s.parts.some(p=>p.text===line.trim())),record.key+line);}
for(let i=0;i<4;i++)for(const block of run(`flowBlocks(${i})`)){const node=run('renderBlock')(block);assert.ok(node);}
const creed=run('renderCreed()');assert.equal(walk(creed).filter(x=>x.attrs['data-variant']).length,2);assert.ok(roles(creed).some(x=>x.attrs['data-speech-role']==='assembly'));
const continuation=run("renderBlock({key:'test',tocId:'test',variant:{title:'참회',text:'◎ 형제들에게 고백하오니\\n제 탓이오'},fragmentText:'제 탓이오',fragmentRole:'assembly'})");assert.equal(roles(continuation)[0].attrs['data-speech-role'],'assembly');
run("kyrieView='invocations'");const kyrie=run("renderPrayerFrame('자비송','자비송')");assert.equal(roles(kyrie).filter(x=>x.attrs['data-speech-role']==='assembly').length,4);
assert.ok(html.includes('font-weight: var(--draft-response-weight)'));assert.ok(html.includes('color: var(--draft-guide-ink)'));assert.ok(!/style="|!important/.test(html));
console.log('PASS: separate highlighted assembly cards, three priest greeting choices + one common response, two confession response groups with embedded guidance, all reference ◎ markers, every part renders, creed internal cards, continuation role, invocation responses.');

mode.value='regular';const regular=run("renderBlock(flowBlocks(0).find(b=>b.group==='참회 예식'))");assert.equal(walk(regular).filter(x=>x.classList.contains('reader__guidance')).length,0);assert.ok(roles(regular).some(x=>x.textContent.includes('빌어 주소서')));mode.value='beginner';
console.log('PASS: regular mode hides guidance while preserving assembly text.');
