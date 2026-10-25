from pathlib import Path
import re
s=Path('review/02-ia-v15.html').read_text(encoding='utf-8').replace('검토 v15','검토 v16')
s=s.replace('--draft-choice-card-z:', '--draft-marker-width: 1.25rem; --draft-marker-gap: .375rem; --draft-choice-card-z:',1)
s=s.replace(' .reader__speech-text {', ''' .reader__speech-row { display: grid; grid-template-columns: var(--draft-marker-width) minmax(0, 1fr); column-gap: var(--draft-marker-gap); }
 .reader__speech-marker { text-align: center; }
 .reader__guidance--in-speech { margin-inline-start: calc(var(--draft-marker-width) + var(--draft-marker-gap)); }
 .reader__speech-text {''',1)
old="parts.forEach(part=>{const p=document.createElement('p');p.className=part.kind==='guide' && segment.kind!=='guide'?'reader__speech-text reader__guidance':'reader__speech-text';p.textContent=part.kind==='guide'?'안내 · '+part.text.replace(/^\\[(?:안내|프레임 안내|자료 안내)\\]\\s*|^인쇄본 안내:\\s*/,''):part.text;card.append(p);});"
new=r'''parts.forEach(part=>{
   if(part.kind==='guide'){const p=document.createElement('p');p.className=segment.kind==='guide'?'reader__speech-text':'reader__speech-text reader__guidance reader__guidance--in-speech';p.textContent='안내 · '+part.text.replace(/^\[(?:안내|프레임 안내|자료 안내)\]\s*|^인쇄본 안내:\s*/,'');card.append(p);return;}
   const row=document.createElement('div');row.className='reader__speech-row';
   const match=part.text.match(/^([+◎◆○●])\s*/);const marker=document.createElement('span');marker.className='reader__speech-marker';marker.setAttribute('aria-hidden','true');marker.textContent=match?match[1]:'';
   const p=document.createElement('p');p.className='reader__speech-text';p.textContent=match?part.text.slice(match[0].length):part.text;row.append(marker,p);card.append(row);
    });'''.replace(chr(92)*2,chr(92))
assert old in s
s=s.replace(old,new,1)
s=s.replace("if(segment.kind==='assembly')card.setAttribute('aria-label','합송');", "if(['assembly','priest','lector'].includes(segment.kind))card.setAttribute('aria-label',({assembly:'합송',priest:'사제의 부분',lector:'독서자의 부분'})[segment.kind]);",1)
Path('review/02-ia-v16.html').write_text(s,encoding='utf-8',newline='\r\n')
Path('work/review-ia-v16-check.js').write_text(re.search(r'<script>(.*?)</script>',s,re.S).group(1),encoding='utf-8')

