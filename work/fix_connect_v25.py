from pathlib import Path
p=Path('work/connect_remaining_v25.py');s=p.read_text(encoding='utf-8');a=s.index('a=s.index(');b=s.index('s=s.replace("const compactScore',a);s=s[:a]+'''old="if(prayerId==='신앙의 신비여'){const response=memorialResponse();return find('slot')"
if old in s:
 a=s.index(old,s.index('function scoreAssets'));b=s.index('return (prayerId',a)
 s=s[:a]+"if(prayerId==='신앙의 신비여'){const season=currentSeason()?.key;return find('slot').value==='main' && season?(reengravedPrincipalScores[prayerId]||[]).filter(asset=>asset.season===season):[];}"+s[b:]
'''+s[b:];p.write_text(s,encoding='utf-8',newline='\r\n')
