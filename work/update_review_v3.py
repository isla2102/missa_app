from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
html = (root/'review/02-ia-v2.html').read_text(encoding='utf-8')
html = html.replace('검토 v2', '검토 v3')
data = '''
const contents = [
 [['입당 성가',0],['성호경',0],['인사',0],['참회 예식',1],['자비송',1],['대영광송',1],['본기도',1]],
 [['제1독서',0],['화답송',0],['제2독서',0],['복음 환호송',1],['복음',1],['강론',2],['신앙 고백',2],['보편 지향 기도',3]],
 [['예물 준비 · 봉헌 성가',0],['예물 기도',0],['감사 기도',1],['주님의 기도',2],['평화 예식',2],['영성체 예식 · 영성체 성가',3],['영성체 후 기도',3]],
 [['공지 사항',0],['강복',0],['파견',1],['파견 성가',1]]
].map((items, partIndex) => items.map(([title, page], index) => ({id:`part-${partIndex}-item-${index}`, title, page})));
let selectedItem = null;
function jumpToItem(partIndex, item) {
 part = partIndex; spread = Math.floor(item.page / 2); selectedItem = item.id;
 render(); find('drawer').close();
}
'''
html = html.replace('let part = 0, spread = 0, opener = null;', data+'\nlet part = 0, spread = 0, opener = null;')
old = "const h = document.createElement('h3'); h.className = 'reader__page-title'; h.textContent = title;"
new = """const h = document.createElement('h3'); h.className = 'reader__page-title'; h.textContent = title;
  const list = document.createElement('ul');
  contents[part].filter(item => item.page === spread * 2 + i).forEach(item => {
   const li = document.createElement('li'); li.id = item.id; li.tabIndex = -1;
   li.textContent = item.title;
   if (item.id === selectedItem) { li.setAttribute('aria-current','location'); li.textContent += ' ← 選択位置'.replace('選択位置','선택 위치'); }
   list.append(li);
  });"""
html = html.replace(old,new).replace('page.append(h,p,note);','page.append(h,list,p,note);')
old = "if (which === 'toc') parts.forEach((item,i) => { const p = document.createElement('p'); const b = document.createElement('button'); b.type = 'button'; b.textContent = item.title; if (part === i) b.setAttribute('aria-current','step'); b.onclick = () => { go(i); find('drawer').close(); }; p.append(b); body.append(p); });"
new = """if (which === 'toc') {
  text('예식별 세부 순서입니다. 항목을 누르면 해당 순서가 있는 두 페이지로 이동합니다. 적용 여부가 달라지는 항목은 실제 전례 데이터에 따라 조정할 예정입니다.');
  const nav = document.createElement('nav'); nav.setAttribute('aria-label','미사 전체 세부 목차');
  parts.forEach((item, partIndex) => {
   const group = document.createElement('section'); const heading = document.createElement('h3'); heading.textContent = item.title;
   const list = document.createElement('ol');
   contents[partIndex].forEach(entry => {
    const li = document.createElement('li'); const button = document.createElement('button'); button.type = 'button';
    button.textContent = entry.title;
    if (entry.id === selectedItem || (!selectedItem && partIndex === part && entry.page === spread * 2 && entry === contents[partIndex].find(x => x.page === spread * 2))) button.setAttribute('aria-current','location');
    button.onclick = () => jumpToItem(partIndex,entry); li.append(button); list.append(li);
   });
   group.append(heading,list); nav.append(group);
  }); body.append(nav);
 }"""
assert old in html
html = html.replace(old,new)
html = html.replace('function go(index) { part = index;', 'function go(index) { selectedItem = null; part = index;')
html = html.replace('spread = Math.max(0,spread-1); render();','selectedItem = null; spread = Math.max(0,spread-1); render();')
html = html.replace('spread = Math.min(Math.ceil(parts[part].pages.length/2)-1,spread+1); render();','selectedItem = null; spread = Math.min(Math.ceil(parts[part].pages.length/2)-1,spread+1); render();')
html = html.replace("li.textContent += ' ← 選択位置'.replace('選択位置','선택 위치');", "li.textContent += ' ← 선택 위치';")
html = html.replace("find('drawer').addEventListener('close', () => opener?.focus());", "find('drawer').addEventListener('close', () => { const target = selectedItem && document.getElementById(selectedItem); if (target) target.focus({preventScroll:true}); else opener?.focus(); });")
with (root/'review/02-ia-v3.html').open('w',encoding='utf-8',newline='\r\n') as f: f.write(html)
script = re.search(r'<script>(.*?)</script>',html,re.S).group(1)
(root/'work/review-ia-v3-check.js').write_text(script,encoding='utf-8')
# Validate the actual data extracted from the HTML, without needing a browser.
parts_data = re.search(r'const parts = (\[.*?\n\]);',script,re.S).group(1)
contents_data = re.search(r'const contents = (\[.*?\n\]\.map\(.*?;)',script,re.S).group(1)
test = "const assert = require('node:assert/strict');\nconst parts = "+parts_data+";\nconst contents = "+contents_data+'''
assert.equal(contents.length, 4);
const ids = new Set();
let count = 0;
contents.forEach((items, part) => items.forEach(item => {
 assert.ok(item.page >= 0 && item.page < parts[part].pages.length);
 assert.ok(!ids.has(item.id)); ids.add(item.id);
 const spread = Math.floor(item.page / 2);
 assert.ok(item.page >= spread * 2 && item.page < spread * 2 + 2);
 count++;
}));
assert.equal(count,26);
assert.equal(contents[1].find(x=>x.title==='보편 지향 기도').page,3);
assert.equal(Math.floor(contents[1].find(x=>x.title==='보편 지향 기도').page/2),1);
console.log(`PASS: four groups, ${count} unique targets, page ranges and spread mapping`);
'''
(root/'work/test-toc-v3.cjs').write_text(test,encoding='utf-8')
print('Created v3 detailed TOC')
