const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const mode=process.argv[2]||'stills';const out=process.argv[3];
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 await p.goto('file://'+path.resolve(process.env.PAGE||'reel.html'));await p.evaluate(()=>window.ready);await p.waitForTimeout(500);
 if(mode==='stills'){const ts=process.argv.slice(4).map(Number);for(const t of ts){await p.evaluate(t=>render(t),t);await p.screenshot({path:`${out}/still_${t}.png`})}}
 else{const fps=30;const dur=await p.evaluate(()=>DUR);fs.mkdirSync(out,{recursive:true});
  for(let i=0;i<Math.round(dur*fps);i++){await p.evaluate(t=>render(t),i/fps);await p.screenshot({path:`${out}/f_${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:93})}}
 await b.close()})();
