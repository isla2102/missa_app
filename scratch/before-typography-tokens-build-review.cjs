'use strict';
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const read=relative=>fs.readFileSync(path.join(root,relative),'utf8').replace(/^\uFEFF/,'').replace(/\r\n/g,'\n');
function withinReview(file){return typeof file==='string'&&/^review\/[a-zA-Z0-9_-]+\.html$/.test(file);}
function validateConfig(config){
 if(!withinReview(config.output)||!withinReview(config.baseline)||config.output===config.baseline||/^review\/02-ia-v\d+\.html$/.test(config.output))throw Error('Output must be a review HTML distinct from archived baseline');
 for(const [name,binding] of Object.entries(config.bindings||{})){
  if(!/^[a-zA-Z]+$/.test(name)||typeof binding.path!=='string')throw Error('Invalid binding');
  const resolved=path.resolve(root,binding.path);if(!resolved.startsWith(root+path.sep)||path.isAbsolute(binding.path))throw Error('Binding outside project');
 }
}
function jsonForScript(value){return JSON.stringify(value).replace(/</g,'\\u003c').replace(/\u2028/g,'\\u2028').replace(/\u2029/g,'\\u2029');}
function build(config){
 validateConfig(config);const values={};let js=read('review/source/reader.js');
 for(const [name,binding] of Object.entries(config.bindings)){let value=JSON.parse(read(binding.path));if(binding.array)value=[value];values[name]=value;const token='{{'+name+'}}';if(!js.includes(token))throw Error('Missing binding '+name);js=js.replace(token,()=>jsonForScript(value));}
 for(const [name,file] of Object.entries(config.modules||{})){const resolved=path.resolve(root,file);if(!resolved.startsWith(root+path.sep))throw Error('Module outside project');const code=read(file).replace(/\/\/ NODE_EXPORT_START[\s\S]*?\/\/ NODE_EXPORT_END/g,'').replace(/if\(typeof module!=='undefined'\)module\.exports=.*?;\n?/, '');js=js.replace('{{'+name+'}}\n',()=>code);}
 if(/\{\{\w+\}\}/.test(js))throw Error('Unresolved script binding');
 const {validateDocument}=require('../review/source/daily-document.cjs');for(const doc of values.dailyDocuments||[]){const errors=validateDocument(doc,values.dailySources);if(errors.length)throw Error('Invalid daily document: '+errors.join(', '));}
 const css=read('review/source/reader.css');return read('review/source/shell.html').replace('{{READER_CSS}}',()=>css).replace('{{READER_JS}}',()=>js);
}
if(require.main===module){const config=JSON.parse(read('review/source/build.json'));const html=build(config);fs.writeFileSync(path.join(root,config.output),html.replace(/\n/g,'\r\n'),'utf8');console.log('Built '+config.output);}
module.exports={build,validateConfig,jsonForScript};
