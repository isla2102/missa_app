from pathlib import Path
p=Path('work/update_review_v19.py');s=p.read_text(encoding='utf-8')
s=s.replace('function renderAlleluia(){','function renderAlleluia(part=null){')
s=s.replace("section.append(first,choir,response());return section;", "const last=response();section.append(first,choir,last);if(part==='first')section.replaceChildren(row,first);else if(part==='choir')section.replaceChildren(choir);else if(part==='last')section.replaceChildren(last);return section;")
s=s.replace("Path('review/02-ia-v19.html').write_text", "s=s.replace(\"  }else if(item.title==='파견'){\",\"  }else if(item.title==='복음 환호송'){\\n   ['first','choir','last'].forEach((acclamationPart,i)=>blocks.push({key:i?`${item.id}-${acclamationPart}`:item.id,tocId:item.id,acclamationPart}));\\n  }else if(item.title==='파견'){\",1)\ns=s.replace(\" if(block.variant){\",\" if(block.acclamationPart)node=renderAlleluia(block.acclamationPart);\\n else if(block.variant){\",1)\nPath('review/02-ia-v19.html').write_text")
p.write_text(s,encoding='utf-8',newline='\r\n')
# Correct counts: a rest is a MusicXML note element, but not a pitched note.
p=Path('docs/교중미사악보/reengraved/alleluia-365-manifest.json');d=__import__('json').loads(p.read_text(encoding='utf-8'));d['noteCount']=16;d['restCount']=1;d['confirmedHymnNumber']=365;p.write_text(__import__('json').dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
