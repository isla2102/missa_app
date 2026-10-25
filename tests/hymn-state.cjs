const a=require('node:assert/strict'),{readHymnSet,writeHymnSet,parseHymnNumbers}=require('../review/source/hymn-state.cjs');
const data=new Map([['missa-v02-hymn','legacy']]);const storage={getItem:k=>data.get(k)||null,setItem:(k,v)=>data.set(k,v)};
a.deepEqual(parseHymnNumbers('238, 221'),[238,221]);a.throws(()=>parseHymnNumbers('0, 529'));a.throws(()=>parseHymnNumbers('1.5'));
writeHymnSet(storage,'2026-10-18','main',{entrance:[416],offertory:[238,221],communion:[154,153,152],recessional:[63]});
a.deepEqual(readHymnSet(storage,'2026-10-18','main').offertory,[238,221]);a.deepEqual(readHymnSet(storage,'2026-10-19','main').offertory,[]);a.deepEqual(readHymnSet(storage,'2026-10-18','dawn').offertory,[]);a.equal(data.get('missa-v02-hymn'),'legacy');a.throws(()=>writeHymnSet(storage,'bad','main',{}));
data.set('missa.hymns.v1:2026-10-18:main','bad');a.deepEqual(readHymnSet(storage,'2026-10-18','main').entrance,[]);console.log('PASS hymn arrays, validation, date/slot isolation, legacy preservation, corrupt storage.');

const {readLegacyHymnNumbers}=require('../review/source/hymn-state.cjs');data.set('missa-v02-hymn|2026-10-18|home|main|입당',JSON.stringify({number:'416',title:'old',lyrics:'memo'}));a.equal(readLegacyHymnNumbers(storage,'2026-10-18','main').entrance[0],416);a.equal(readLegacyHymnNumbers(storage,'2026-10-19','main'),null);a.equal(JSON.parse(data.get('missa-v02-hymn|2026-10-18|home|main|입당')).lyrics,'memo');console.log('PASS exact legacy home/date/slot mapping, original metadata unchanged.');
