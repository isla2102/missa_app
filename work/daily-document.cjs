'use strict';
function validateDocument(doc,sources={}){
 const errors=[];const fail=m=>errors.push(m);const keys=(v,allowed)=>{if(!v||typeof v!=='object'||Array.isArray(v))return false;for(const k of Object.keys(v))if(!allowed.includes(k))fail('unexpected field: '+k);return true;};
 if(!keys(doc,['schemaVersion','documentId','date','observance','sourceRefs','sections']))return ['invalid document'];
 if(doc.schemaVersion!==1||typeof doc.documentId!=='string'||!doc.documentId)fail('document header');
 if(typeof doc.date!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(doc.date)||!Number.isFinite(Date.parse(doc.date))||new Date(doc.date).toISOString().slice(0,10)!==doc.date)fail('date');
 if(typeof doc.observance!=='string'||!doc.observance)fail('observance');
 if(!Array.isArray(doc.sourceRefs)||!doc.sourceRefs.length||doc.sourceRefs.some(k=>!Object.hasOwn(sources,k)))fail('sources');
 const ids=new Set();const id=v=>{if(typeof v!=='string'||!v||ids.has(v))fail('duplicate/invalid id');ids.add(v);};
 if(!Array.isArray(doc.sections)||!doc.sections.length)return [...errors,'sections'];
 for(const s of doc.sections){if(!keys(s,['id','kind','title','status','paragraphs'])){fail('section');continue;}id(s.id);
  if(!['reading','gospel','psalm','acclamation','prayer','intercession','preface','antiphon'].includes(s.kind)||typeof s.title!=='string'||!s.title)fail('section header');
  if(!['verified','missing','needs-review'].includes(s.status))fail('status');
  if(!Array.isArray(s.paragraphs)){fail('paragraphs');continue;}if(s.status==='verified'&&!s.paragraphs.length)fail('empty verified');
  for(const p of s.paragraphs){if(!keys(p,['id','role','text','sourceRef'])){fail('paragraph');continue;}id(p.id);if(!['text','priest','lector','assembly','guidance'].includes(p.role)||typeof p.text!=='string'||!p.text.trim())fail('paragraph content');if(!Object.hasOwn(sources,p.sourceRef)||!doc.sourceRefs?.includes(p.sourceRef))fail('sourceRef');}
 }
 return errors;
}
function selectDocument(documents,date){return documents.find(d=>d.date===date)||null;}
function resolveAnchor(doc,anchor){const section=doc.sections.find(s=>s.id===anchor?.sectionId)||doc.sections[0];const p=section.paragraphs.find(p=>p.id===anchor?.paragraphId)||section.paragraphs[0];return {sectionId:section.id,paragraphId:p?.id||null,offset:Math.min(Math.max(0,Number.isFinite(anchor?.offset)?anchor.offset:0),p?.text.length||0)};}
if(typeof module!=='undefined')module.exports={validateDocument,selectDocument,resolveAnchor};
