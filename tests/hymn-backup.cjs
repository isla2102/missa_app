const a=require('node:assert/strict'),m=require('../review/source/hymn-backup.cjs');
const data=new Map(),s={get length(){return data.size},key:i=>[...data.keys()][i],getItem:k=>data.get(k)??null,setItem:(k,v)=>data.set(k,v),removeItem:k=>data.delete(k)};
const set={entrance:[416],offertory:[238,221],communion:[154,153,152],recessional:[63]};
s.setItem('missa.hymns.v1:2026-10-18:main',JSON.stringify(set));s.setItem('missa-v02-hymn','legacy');
const backup=m.exportHymnBackup(s);a.equal(backup.records.length,1);a.deepEqual(m.parseHymnBackup(JSON.stringify(backup)).records[0].hymns,set);
a.throws(()=>m.parseHymnBackup('{'));a.throws(()=>m.parseHymnBackup(JSON.stringify({...backup,version:99})));a.throws(()=>m.parseHymnBackup(JSON.stringify({...backup,records:[{...backup.records[0],date:'2026-02-30'}]})));a.throws(()=>m.parseHymnBackup(JSON.stringify({...backup,records:[...backup.records,...backup.records]})));
const imported=JSON.parse(JSON.stringify(backup));imported.records[0].hymns.entrance=[1];m.restoreHymnBackup(s,imported);a.equal(JSON.parse(s.getItem('missa.hymns.v1:2026-10-18:main')).entrance[0],1);a.equal(s.getItem('missa-v02-hymn'),'legacy');
const raw=s.getItem('missa.hymns.v1:2026-10-18:main');const fail={...s,setItem:()=>{throw Error('quota')}};a.throws(()=>m.restoreHymnBackup(fail,backup));a.equal(s.getItem('missa.hymns.v1:2026-10-18:main'),raw);
console.log('PASS backup roundtrip, malformed/version/date/duplicate rejection, restore, legacy preservation and storage failure.');

const original=JSON.stringify(set),key='missa.hymns.v1:2026-10-18:main';s.setItem(key,original);let calls=0;const partial={getItem:k=>s.getItem(k),removeItem:k=>s.removeItem(k),setItem:(k,v)=>{if(++calls===2)throw Error('quota');s.setItem(k,v);}};a.throws(()=>m.restoreHymnBackup(partial,{...backup,records:[imported.records[0],{date:'2026-10-19',slot:'main',hymns:set}]}));a.equal(s.getItem(key),original);a.equal(s.getItem('missa.hymns.v1:2026-10-19:main'),null);console.log('PASS multi-record rollback after second write failure.');
