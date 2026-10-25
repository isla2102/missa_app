const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const html=fs.readFileSync(process.env.MISSA_REVIEW_FILE||'review/02-ia-current.html','utf8'),js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const walk=n=>[n,...n.children.flatMap(walk)];
class E{
 constructor(t){this.tagName=t;this.children=[];this.attrs={};this._text='';this.className='';this.classList={contains:c=>this.className.split(' ').includes(c),add:c=>{if(!this.classList.contains(c))this.className+=' '+c}};}
 get textContent(){return this._text+this.children.map(n=>n.textContent).join('')}set textContent(t){this._text=t;this.children=[]}
 append(...n){n.forEach(x=>{const old=x.parentElement;if(old){const i=old.children.indexOf(x);if(i>=0)old.children.splice(i,1);}x.parentElement=this;this.children.push(x);});}replaceChildren(...n){this._text='';this.children=[];this.append(...n)}
 replaceWith(n){const p=this.parentElement;if(p){p.children.splice(p.children.indexOf(this),1,n);n.parentElement=p;}}
 insertBefore(n,b){n.parentElement=this;this.children.splice(this.children.indexOf(b),0,n)}setAttribute(k,v){this.attrs[k]=v}getAttribute(k){return this.attrs[k]}addEventListener(){}closest(){return null}focus(){}
 querySelectorAll(s){return walk(this).slice(1).filter(x=>s[0]==='.'?x.classList.contains(s.slice(1)):x.tagName===s)}querySelector(s){return this.querySelectorAll(s)[0]}
}
const date={value:'2026-10-18'};const ui=new Map();
const slot={value:'main',selectedOptions:[{textContent:'교중미사'}]},mode={value:'beginner'};
const sandbox={document:{createElement:t=>new E(t),createElementNS:(_,t)=>new E(t),querySelector:s=>{if(s.includes('mode'))return mode;if(s.includes('slot'))return slot;if(s.includes('date'))return date;const key=s.match(/data-js="(.*?)"/)?.[1];if(!ui.has(key)){const e=new E('div');e.showModal=()=>e.open=true;e.close=()=>e.open=false;ui.set(key,e);}return ui.get(key);}}};
const windowEvents={};const raf=[];const saved=new Map([['missa.reader.symbol-tutorial.v1','done'],['missa.reader.position.v1:2026-10-18',JSON.stringify({version:1,date:'2026-10-18',part:1,anchor:'part-1-item-4',mode:'regular',slot:'youth',scrolls:{}})]]);
E.prototype.addEventListener=function(name,fn){(this.events||(this.events={}))[name]=fn;};E.prototype.focus=function(){this.focused=true;};
sandbox.document.querySelectorAll=()=>[];sandbox.document.querySelector('[data-js="book"]').clientWidth=0;
sandbox.window={addEventListener:(name,fn)=>windowEvents[name]=fn};sandbox.localStorage={getItem:key=>saved.get(key)||null,setItem:(key,value)=>saved.set(key,value)};sandbox.requestAnimationFrame=fn=>{raf.push(fn);return raf.length;};sandbox.cancelAnimationFrame=()=>{};
vm.createContext(sandbox);vm.runInContext(js,sandbox);const run=code=>vm.runInContext(code,sandbox);
assert.equal(run('part'),1);assert.equal(run('currentAnchor'),'part-1-item-4');assert.equal(mode.value,'regular');assert.equal(slot.value,'youth');
assert.equal(typeof ui.get('header-menu').onclick,'function');assert.equal(typeof ui.get('viewport-reset').onclick,'function');assert.equal(typeof windowEvents.pagehide,'function');assert.equal(typeof windowEvents.resize,'function');
run("find('score-modal-body')");ui.get('score-modal-body').append(new E('img'));ui.get('score-modal').events.close();assert.equal(ui.get('score-modal-body').children.length,0);assert.equal(ui.get('part-next').focused,true);
ui.get('viewport-reset').onclick();assert.equal(run('viewerOrientation'),'auto');assert.ok(ui.get('part-next').focused);
windowEvents.resize();assert.ok(raf.length>0);
console.log('PASS full script boot, saved state application, close focus/cleanup, reset focus and resize wiring (mock geometry).');
