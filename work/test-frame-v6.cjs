const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const file = path.join(__dirname,'../review/02-ia-v6.html');
assert.ok(fs.existsSync(file), 'v6 frame review must exist');
const html = fs.readFileSync(file,'utf8');
const js = html.match(/<script>([\s\S]*?)<\/script>/)[1];
class Element {
 constructor(tag) { this.tagName=tag; this.children=[]; this.attrs={}; this.textContent=''; }
 append(...nodes) { this.children.push(...nodes); }
 setAttribute(key,value) { this.attrs[key]=value; }
}
const mode = {value:'beginner'};
const sandbox = {document:{createElement:tag=>new Element(tag),querySelector:()=>mode}};
vm.createContext(sandbox);
vm.runInContext(js.slice(0,js.indexOf("find('part-prev').onclick")),sandbox);
const value = code => vm.runInContext(code,sandbox);
assert.equal(value('contents.flat().length'),26);
assert.equal(value('contents.flat().every(item=>Boolean(frameSpecs[item.title]))'),true);
assert.equal(value("frameSpecs['성호경'].kind"),'fixed');
assert.equal(value("frameSpecs['인사'].kind"),'choice');
assert.equal(value("frameSpecs['본기도'].kind"),'proper');
assert.equal(value("frameSpecs['입당 성가'].source"),'hymnSet');
let checks=0;
for (const [title, card] of [['성호경',false],['인사',false],['본기도',true],['입당 성가',true]]) {
 const frame = value(`renderItem(contents.flat().find(item=>item.title===${JSON.stringify(title)}))`);
 assert.equal(frame.tagName,'section');
 assert.equal(frame.children[0].tagName,'h3');
 assert.equal(frame.children.some(x=>x.className==='reader__content-card'),card,title);
 checks++;
}
const titles = value('JSON.stringify(contents.flat().map(x=>x.title))');
for(const title of JSON.parse(titles)) {
 const frame = value(`renderItem(contents.flat().find(item=>item.title===${JSON.stringify(title)}))`);
 assert.equal(frame.children[0].textContent.startsWith(title),true);
}
assert.equal(js.includes('fetch('),false,'No unimplemented source integration should be presented as real');
console.log(`PASS: 26 mapped frames; four rendering branches; source separation; ${checks} card/no-card cases; no fake network integration`);
