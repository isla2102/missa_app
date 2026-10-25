from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
html = (root/'review/02-ia-v3.html').read_text(encoding='utf-8')
html = html.replace('검토 v3','검토 v4')
html = html.replace('</style>', '''@layer components {
 .reader__toc-link { display: inline-block; min-height: 1.5rem; padding-block: .125rem; }
 .reader__toc-link[aria-current="location"] { font-weight: bold; text-decoration-thickness: 2px; }
}
</style>''')
html = html.replace('min-height: 1.5rem; padding-block: .125rem;', 'min-height: var(--draft-toc-target); padding-block: var(--draft-toc-gap);')
html = html.replace('--draft-gap: .75rem;', '--draft-toc-target: 1.5rem; --draft-toc-gap: .125rem; --draft-gap: .75rem;')
html = html.replace('function render() {\n const current', '''function render() {
 if (!contents[part].some(item => item.id === selectedItem && Math.floor(item.page / 2) === spread)) {
  selectedItem = contents[part].find(item => item.page === spread * 2)?.id ?? null;
 }
 const current''')
old = '''const li = document.createElement('li'); const button = document.createElement('button'); button.type = 'button';
    button.textContent = entry.title;
    if (entry.id === selectedItem || (!selectedItem && partIndex === part && entry.page === spread * 2 && entry === contents[partIndex].find(x => x.page === spread * 2))) button.setAttribute('aria-current','location');
    button.onclick = () => jumpToItem(partIndex,entry); li.append(button); list.append(li);'''
new = '''const li = document.createElement('li'); const link = document.createElement('a');
    link.className = 'reader__toc-link'; link.href = `#${entry.id}`; link.textContent = entry.title;
    if (entry.id === selectedItem) { link.setAttribute('aria-current','location'); link.textContent += ' · 현재 위치'; }
    link.onclick = event => { event.preventDefault(); jumpToItem(partIndex,entry); }; li.append(link); list.append(li);'''
assert old in html
html = html.replace(old,new)
with (root/'review/02-ia-v4.html').open('w',encoding='utf-8',newline='\r\n') as f: f.write(html)
js = re.search(r'<script>(.*?)</script>',html,re.S).group(1)
(root/'work/review-ia-v4-check.js').write_text(js,encoding='utf-8')
assert "link.href = `#${entry.id}`" in js
assert "link.setAttribute('aria-current','location')" in js
assert "const button = document.createElement('button')" not in js
assert 'reader__toc-link[aria-current="location"]' in html
assert 'min-height: var(--draft-toc-target)' in html
print('PASS: semantic fragment links, current location marker, compact target and emphasis')
