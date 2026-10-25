'use strict';
const {spawnSync}=require('node:child_process'),path=require('node:path'),fs=require('node:fs');
const root=path.resolve(__dirname,'..');
const scripts=['tools/build-review.cjs','tests/build-review.cjs','tests/daily-document.cjs','tests/reader-state.cjs','tests/reader-boot.cjs','tests/reader-regression.cjs','tests/reference-catalogs.cjs','tests/content-readiness.cjs','tests/hymn-state.cjs','tests/hymn-backup.cjs'];
const logs=[];
for(const script of scripts){const result=spawnSync(process.execPath,[script],{cwd:root,encoding:'utf8'});logs.push('$ node '+script+'\n'+result.stdout+result.stderr);if(result.status!==0){fs.writeFileSync(path.join(root,'work/review-check.log'),logs.join('\n'));process.stdout.write(logs.at(-1));process.exit(result.status||1);}console.log('PASS '+script);}
fs.writeFileSync(path.join(root,'work/review-check.log'),logs.join('\n'));console.log('PASS all 10 commands; details: work/review-check.log');
