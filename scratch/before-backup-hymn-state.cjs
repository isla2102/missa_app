const hymnRoles=['entrance','offertory','communion','recessional'];
function parseHymnNumbers(text){if(!String(text).trim())return [];const parts=String(text).trim().split(/[\s,·]+/);if(parts.some(x=>!/^\d+$/.test(x)||Number(x)<1||Number(x)>528))throw Error('1부터 528 사이의 번호를 쉼표로 구분해 주세요.');return [...new Set(parts.map(Number))];}
function hymnStorageKey(date,slot){if(!/^\d{4}-\d{2}-\d{2}$/.test(date)||!['main','dawn','youth'].includes(slot))throw Error('Invalid hymn context');return 'missa.hymns.v1:'+date+':'+slot;}
function cleanHymnSet(value){const out={};for(const role of hymnRoles){const numbers=value?.[role]||[];if(!Array.isArray(numbers)||numbers.some(n=>!Number.isInteger(n)||n<1||n>528))throw Error('Invalid hymn numbers');out[role]=[...new Set(numbers)];}return out;}
function readHymnSet(storage,date,slot){try{return cleanHymnSet(JSON.parse(storage.getItem(hymnStorageKey(date,slot))));}catch{return cleanHymnSet(null);}}
function writeHymnSet(storage,date,slot,value){const key=hymnStorageKey(date,slot),set=cleanHymnSet(value);storage.setItem(key,JSON.stringify(set));return set;}
if(typeof module!=='undefined')module.exports={parseHymnNumbers,readHymnSet,writeHymnSet};
