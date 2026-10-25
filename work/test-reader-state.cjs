const assert=require('node:assert/strict');const {readState,writeState}=require('./reader-state.cjs');
const m=new Map();const storage={getItem:k=>m.get(k)||null,setItem:(k,v)=>m.set(k,v)};
const state={version:1,date:'2026-10-18',part:1,anchor:'part-1-item-0',mode:'beginner',slot:'main',scrolls:{'part-1-item-0:0':0.65}};
assert.equal(writeState(storage,state),true);assert.deepEqual(readState(storage,state.date),state);assert.equal(readState(storage,'2026-10-19'),null);
m.set('missa.reader.position.v1:2026-10-18','{broken');assert.equal(readState(storage,state.date),null);
m.set('missa.reader.position.v1:2026-10-18',JSON.stringify({...state,part:99}));assert.equal(readState(storage,state.date),null);
assert.equal(writeState({setItem(){throw Error('quota')}},state),false);assert.equal(readState({getItem(){throw Error('denied')}},state.date),null);
assert.equal(writeState(storage,{...state,scrolls:{x:2}}),false);console.log('PASS state roundtrip, date isolation, corrupt data, bounds, storage failure.');
