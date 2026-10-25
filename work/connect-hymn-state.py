from pathlib import Path
import json
def save(p,s):Path(p).write_bytes(s.replace('\r\n','\n').replace('\n','\r\n').encode())
p='review/source/build.json';c=json.loads(Path(p).read_text(encoding='utf-8'));c['modules']['HYMN_STATE']='review/source/hymn-state.cjs';c['baseline']='review/02-ia-v56.html';save(p,json.dumps(c,ensure_ascii=False,indent=2)+'\n')
p='review/source/reader.js';s=Path(p).read_text(encoding='utf-8');s=s.replace('const hymnAssignments={};', '''{{HYMN_STATE}}
const hymnTitles={'입당 성가':'entrance','봉헌 성가':'offertory','영성체 성가':'communion','파견 성가':'recessional'};
function currentHymns(){return readHymnSet(localStorage,find('date').value,find('slot').value);}
function saveCurrentHymns(value){return writeHymnSet(localStorage,find('date').value,find('slot').value,value);}
function appendHymnEditor(body){
 const heading=document.createElement('p');heading.textContent=find('date').value+' · '+selectedSlotName()+' · 사용자 편성';body.append(heading);
 const form=document.createElement('form'),inputs={},status=document.createElement('p');status.setAttribute('role','status');
 for(const [title,role] of Object.entries(hymnTitles)){const label=document.createElement('label');label.textContent=title;const input=document.createElement('input');input.type='text';input.setAttribute('aria-label',title+' 편성 번호');input.value=currentHymns()[role].join(', ');inputs[role]=input;label.append(input);form.append(label);}
 const save=document.createElement('button');save.type='submit';save.textContent='편성 저장';form.append(save);body.append(form,status);
 let undo=null;const undoButton=document.createElement('button');undoButton.type='button';undoButton.textContent='적용 취소';undoButton.hidden=true;body.append(undoButton);
 const commit=value=>{try{const previous=currentHymns();saveCurrentHymns(value);undo=previous;for(const role of hymnRoles)inputs[role].value=value[role].join(', ');undoButton.hidden=false;status.textContent='저장했습니다.';scheduleReflow(currentAnchor);return true;}catch{status.textContent='저장하지 못했습니다. 브라우저 저장소 설정을 확인해 주세요.';return false;}};
 form.onsubmit=event=>{event.preventDefault();try{const value={};for(const role of hymnRoles)value[role]=parseHymnNumbers(inputs[role].value);commit(value);}catch(error){status.textContent=error.message;}};
 undoButton.onclick=()=>{if(undo&&commit(undo)){undo=null;undoButton.hidden=true;status.textContent='이전 편성으로 복원했습니다.';}};
 const day=hymnScheduleCatalog.days.find(day=>day.date===find('date').value);if(day){const preview=document.createElement('button');preview.type='button';preview.textContent='추천 적용 검토';body.append(preview);preview.onclick=()=>{const box=document.createElement('div');for(const [title,role] of Object.entries(hymnTitles)){const p=document.createElement('p');p.textContent=title+' · '+(currentHymns()[role].join(', ')||'미등록')+' → '+(day.recommendations[role].join(', ')||'미등록');box.append(p);}const apply=document.createElement('button');apply.type='button';apply.textContent='이 회차에 적용';apply.onclick=()=>{if(commit(day.recommendations))box.remove();};const cancel=document.createElement('button');cancel.type='button';cancel.textContent='닫기';cancel.onclick=()=>box.remove();box.append(apply,cancel);body.append(box);};}
}''')
s=s.replace("input.type='number';input.min='1';input.max='528';input.step='1';input.required=true;", "input.type='text';")
s=s.replace("hymnAssignments[hymnAssignmentKey(headingTitle)]||''", "currentHymns()[hymnTitles[headingTitle]].join(', ')")
s=s.replace("const number=hymnAssignments[hymnAssignmentKey(headingTitle)];if(number){scroll.append(renderPhoto(hymnScoreAsset(number,headingTitle)));", "const numbers=currentHymns()[hymnTitles[headingTitle]];if(numbers.length){numbers.forEach(number=>scroll.append(renderPhoto(hymnScoreAsset(number,headingTitle))));")
a=s.index(' form.onsubmit=event=>',s.index('function renderHymnScore'));b=s.index('\n row.append(form)',a)
s=s[:a]+" form.onsubmit=event=>{event.preventDefault();try{const numbers=parseHymnNumbers(input.value);saveCurrentHymns({...currentHymns(),[hymnTitles[headingTitle]]:numbers});fill();}catch(error){status.hidden=false;status.textContent=error.message;}};"+s[b:]
s=s.replace("text(`${selectedSlotName()} · 미등록`); ['입당','봉헌','영성체','파견'].forEach(role => text(`${role} 성가 · 미등록`));", "appendHymnEditor(body);")
s=s.replace('v55','v56');save(p,s)
p='review/source/shell.html';save(p,Path(p).read_text(encoding='utf-8').replace('v55','v56'))
