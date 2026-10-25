function validReaderState(s,date){return !!s&&s.version===1&&s.date===date&&/^\d{4}-\d{2}-\d{2}$/.test(date)&&Number.isInteger(s.part)&&s.part>=0&&s.part<4&&typeof s.anchor==='string'&&/^part-\d-item-\d[\w-]*$/.test(s.anchor)&&['beginner','regular'].includes(s.mode)&&['dawn','main','youth'].includes(s.slot)&&s.scrolls&&typeof s.scrolls==='object'&&!Array.isArray(s.scrolls)&&Object.keys(s.scrolls).length<=100&&Object.values(s.scrolls).every(v=>Number.isFinite(v)&&v>=0&&v<=1);}
function readState(storage,date){try{const raw=storage.getItem('missa.reader.position.v1:'+date);if(!raw||raw.length>20000)return null;const s=JSON.parse(raw);return validReaderState(s,date)?s:null;}catch{return null;}}
function writeState(storage,state){if(!validReaderState(state,state?.date))return false;try{storage.setItem('missa.reader.position.v1:'+state.date,JSON.stringify(state));return true;}catch{return false;}}



if(typeof module!=='undefined')module.exports={readState,writeState};
