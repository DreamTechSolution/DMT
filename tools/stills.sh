#!/bin/bash
# Render the last frame of every scene of <serie_dir>/v<n>.html into <out.png> (contact sheet) for visual QA.
# Usage: tools/stills.sh <serie_dir> <n> <out.png>
set -e; SD=$1; N=$2; OUT=$3; cd "$SD"; T=$(mktemp -d)
node -e "
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('PAGE ERROR',e.message));
await p.goto('file://'+path.resolve('v$N.html'));await p.evaluate(()=>window.ready);const W=await p.evaluate(()=>TIMING.W);
let i=0;for(const k of Object.keys(W)){if(k==='I')continue;await p.evaluate(t=>render(t),W[k][1]-0.4);await p.screenshot({path:'$T/s_'+String(i++).padStart(2,'0')+'.png'})}
console.log('duration',await p.evaluate(()=>DUR));await b.close()})();"
ffmpeg -v error -y -pattern_type glob -i "$T/s_*.png" -vf "scale=240:-1,tile=9x1" -frames:v 1 "$OUT"; rm -rf $T
