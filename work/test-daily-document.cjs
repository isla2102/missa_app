const assert=require('node:assert/strict');
const api=require('./daily-document.cjs');
const sources={official:{url:'https://missa.cbck.or.kr/DailyMissa/20261018'}};
const doc={schemaVersion:1,documentId:'mass-2026-10-18',date:'2026-10-18',observance:'전교 주일',sourceRefs:['official'],sections:[{id:'reading-1',kind:'reading',title:'제1독서',status:'verified',paragraphs:[{id:'reading-1-p1',role:'text',text:'확인된 본문',sourceRef:'official'}]}]};
assert.deepEqual(api.validateDocument(doc,sources),[]);
assert.equal(api.selectDocument([doc],'2026-10-19'),null);
assert.equal(api.selectDocument([doc],doc.date),doc);
const clone=()=>JSON.parse(JSON.stringify(doc));
let bad=clone();bad.sections.push(clone().sections[0]);assert.ok(api.validateDocument(bad,sources).length);
bad=clone();bad.sections[0].paragraphs[0].sourceRef='unknown';assert.ok(api.validateDocument(bad,sources).length);
bad=clone();bad.date='2026-02-30';assert.ok(api.validateDocument(bad,sources).length);
bad=clone();bad.sections[0].paragraphs[0].text='';assert.ok(api.validateDocument(bad,sources).length);
bad=clone();bad.bodyOverride='other';assert.ok(api.validateDocument(bad,sources).length);
assert.equal(api.resolveAnchor(doc,{sectionId:'gone',paragraphId:'gone',offset:0}).sectionId,'reading-1');
assert.equal(api.resolveAnchor(doc,{sectionId:'reading-1',paragraphId:'reading-1-p1',offset:999}).offset,6);
console.log('PASS document validation, date isolation, duplicate IDs, source refs, missing text, override rejection, anchor fallback.');

const fixture=require("../data/days/2026-10-18.json");const refs=require("../data/sources.json");assert.deepEqual(api.validateDocument(fixture,refs),[]);console.log("PASS real fixture cross references.");
