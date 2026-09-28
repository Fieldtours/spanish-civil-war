// node shoot.js jobs.json  -> renders each job to its .out path
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const jobs=JSON.parse(fs.readFileSync(process.argv[2]));
const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
for(const j of jobs){const p=await (await b.newContext({viewport:{width:j.w,height:j.h},deviceScaleFactor:1})).newPage();
 const errs=[];p.on('console',m=>{if(/maperr|rror/.test(m.text()))errs.push(m.text())});
 await p.goto('http://localhost:8813/render.html?job='+encodeURIComponent(JSON.stringify(j)));
 try{await p.waitForFunction(()=>document.title.startsWith('READY'),{timeout:+(process.env.SHOOT_MS||900000)})}catch(e){console.log('timeout',j.out)}
 await p.waitForTimeout(300);
 const data=await p.evaluate(png=>document.querySelector('canvas').toDataURL(png?'image/png':'image/jpeg',0.85),!!j.png);
 fs.writeFileSync(j.out,Buffer.from(data.split(',')[1],'base64'));console.log(j.out,await p.title(),errs.slice(0,3).join(' | '));await p.close()}
await b.close()})();
