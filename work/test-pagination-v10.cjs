const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const file=path.join(__dirname,'../review/02-ia-v10.html');assert.ok(fs.existsSync(file),'v10 pagination review required');
const html=fs.readFileSync(file,'utf8');const js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const sandbox={document:{querySelector:()=>({})}};vm.createContext(sandbox);
vm.runInContext(js.slice(0,js.indexOf("find('part-prev').onclick")),sandbox);
const run=code=>vm.runInContext(code,sandbox);
const pack=(blocks,height)=>{
 sandbox.fixture=blocks;sandbox.height=height;
 return JSON.parse(run('JSON.stringify(paginateFlow(fixture, trial=>trial.reduce((sum,x)=>sum+x.height,0)<=height, block=>[block]))'));
};
const blocks=[{key:'intro',height:25},{key:'kyrie-score',height:70},{key:'gloria-score',height:70},{key:'collect',height:30}];
let pages=pack(blocks,100);assert.equal(pages.length,2);assert.deepEqual(pages.flatMap(x=>x.blocks.map(b=>b.key)),blocks.map(b=>b.key));assert.ok(pages.every(p=>p.blocks.reduce((s,b)=>s+b.height,0)<=100));
pages=pack(blocks,80);assert.equal(pages.length,4);assert.equal(pages.findIndex(p=>p.blocks.some(b=>b.key==='gloria-score')),2);
assert.equal(run("spreadForAnchor("+JSON.stringify(pages)+", 'gloria-score')"),1);
pages=pack([{key:'long',height:200},{key:'next',height:20}],100);assert.equal(pages[0].oversize,true);assert.equal(pages[1].blocks[0].key,'next');
run("var splitPages=paginateFlow([{key:'prayer',height:200}],trial=>trial.reduce((sum,x)=>sum+x.height,0)<=100,block=>[{...block,key:'prayer',height:90,text:'first'},{...block,key:'prayer-c1',height:90,text:'second'}]);");assert.equal(run('splitPages.length'),2);
assert.equal(run("spreadForAnchor(splitPages,'prayer-c1')"),0);
assert.equal(run('flowBlocks(2).length'),11); // Seven original items plus four separate prayer-score frames.
assert.equal(html.includes('.reader__page { min-height: 0; border: 1px solid; padding: var(--draft-padding); overflow: hidden;'),true);
assert.ok(html.includes('.reader__score-scroll {'));
assert.ok(js.includes("scoreWindow.setAttribute('tabindex','0')"));
assert.ok(js.includes('new ResizeObserver'));
assert.equal(js.includes('Math.floor(item.page / 2)'),false);
console.log('PASS: fit-based packing, ordered content/no loss, resized page counts, anchor relocation, long-block fallback/splitting, nested score frames, hidden page overflow, keyboard-scrollable scores');
