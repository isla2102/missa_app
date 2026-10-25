const assert=require('node:assert/strict');
const {contentReadiness}=require('../review/source/daily-document.cjs');
const docs=[{date:'2026-10-18',sections:[{status:'verified'},{status:'missing'}]}];
const issues={issues:[{date:'2026-10-18'}]},hymns={days:[{date:'2026-10-19'}]};
assert.deepEqual(contentReadiness('2026-10-18',docs,issues,hymns),{body:'partial',bulletin:true,hymns:false});
assert.deepEqual(contentReadiness('2026-10-19',docs,issues,hymns),{body:'missing',bulletin:false,hymns:true});
assert.deepEqual(contentReadiness('2026-11-01',docs,issues,hymns),{body:'missing',bulletin:false,hymns:false});
assert.equal(contentReadiness('2026-10-18',[{date:'2026-10-18',sections:[{status:'verified'}]}],issues,hymns).body,'ready');
console.log('PASS exact-date readiness, partial body, missing month and no neighboring-date fallback.');
