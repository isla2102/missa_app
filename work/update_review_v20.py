from pathlib import Path
p=Path('review/02-ia-v19.html')
s=p.read_text(encoding='utf-8').replace('검토 v19','검토 v20')
s=s.replace(' .reader__season-period[aria-current=', ' .reader__season-help { flex-shrink: 0; }\n .reader__season-period[aria-current=',1)
anchor='<dialog class="reader__tutorial" id="season-dialog"'
pos=s.index(anchor)
s=s[:pos]+'''<dialog class="reader__tutorial" id="season-help-dialog" data-js="season-help-modal" aria-labelledby="season-help-title" aria-describedby="season-help-text"><div class="reader__modal-heading"><h2 id="season-help-title" data-js="season-help-title"></h2><button type="button" data-js="season-help-close">닫기</button></div><p id="season-help-text" data-js="season-help-text"></p><a data-js="season-help-source" target="_blank" rel="noopener noreferrer">전례 시기 설명 출처</a></dialog>
'''+s[pos:]
pos=s.index('function showSeasonModal(trigger)')
s=s[:pos]+'''const seasonMeanings = {
 ordinary: {title:'연중 시기', text:'예수 그리스도의 구원 신비 전체를 묵상하며, 그분의 말씀과 삶을 일상에서 따라 살아가는 시기입니다. 성탄 시기 뒤와 부활 시기 뒤, 두 구간으로 나뉩니다.'},
 lent: {title:'사순 시기', text:'예수님의 수난과 죽음을 묵상하며 부활을 준비하는 시기입니다. 기도와 회개, 절제와 이웃을 위한 나눔으로 하느님께 돌아가도록 초대받습니다.'},
 easter: {title:'부활 시기', text:'예수 그리스도의 부활을 기뻐하며 새 생명과 희망을 나누는 시기입니다. 주님 부활 대축일부터 성령 강림 대축일까지 이어지며, 부활하신 주님의 증인으로 살아가도록 초대받습니다.'}
};
let seasonHelpOpener=null;
function showSeasonHelp(key,trigger){
 const meaning=seasonMeanings[key];if(!meaning)return;
 seasonHelpOpener=trigger;find('season-help-title').textContent=meaning.title+'란?';find('season-help-text').textContent=meaning.text;
 find('season-help-source').href='https://home.catholic.or.kr/pdsm/bbs_view.asp?id=185256&menu=4798';
 find('season-help-modal').showModal();find('season-help-close').focus();
}
'''+s[pos:]
s=s.replace("const p=document.createElement('p');p.textContent=period.description;card.append(h,p);body.append(card);", "const heading=document.createElement('div');heading.className='reader__modal-heading';const help=document.createElement('button');help.type='button';help.className='reader__season-help';help.textContent='?';help.setAttribute('aria-label',period.title+' 의미 알아보기');help.setAttribute('aria-haspopup','dialog');help.setAttribute('aria-controls','season-help-dialog');help.title=period.title+'란?';help.onclick=()=>showSeasonHelp(period.key,help);heading.append(h,help);const p=document.createElement('p');p.textContent=period.description;card.append(heading,p);body.append(card);")
s=s.replace("find('season-modal-close').onclick", "find('season-help-close').onclick=()=>find('season-help-modal').close();\nfind('season-help-modal').addEventListener('close',()=>seasonHelpOpener?.focus());\nfind('season-modal-close').onclick")
Path('review/02-ia-v20.html').write_text(s,encoding='utf-8',newline='\r\n')
t=Path('work/test-reader-v19.cjs').read_text(encoding='utf-8').replace('02-ia-v19.html','02-ia-v20.html')
t+='''\ndate.value='2026-10-18';run('showSeasonModal()');const helpButtons=walk(ui.get('season-modal-body')).filter(n=>n.className==='reader__season-help');assert.equal(helpButtons.length,4);for(const b of helpButtons){assert.equal(b.attrs['aria-haspopup'],'dialog');b.onclick();assert.equal(ui.get('season-help-modal').open,true);assert.ok(ui.get('season-help-title').textContent.endsWith('란?'));assert.ok(ui.get('season-help-text').textContent.length>60);assert.equal(ui.get('season-modal').open,true);}console.log('PASS: four period help buttons, three meanings, nested dialog keeps calendar open.');\n'''
Path('work/test-reader-v20.cjs').write_text(t,encoding='utf-8',newline='\r\n')
import re
Path('work/review-ia-v20-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
