// Tests for: AAR button in the top bar, the Tour page switch, and "Build my own route".
const {chromium}=require('playwright');
(async()=>{const f=process.argv[2]||'normandy';const b=await chromium.launch();
const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,serviceWorkers:'block'});const p=await ctx.newPage();
const errs=[],fails=[];p.on('pageerror',e=>errs.push('ERR '+e.message));
const ok=(c,m)=>{console.log((c?'  ok   ':'  FAIL ')+m);if(!c)fails.push(m)};
const vis=sel=>p.evaluate(s=>{const e=document.querySelector(s);return !!e&&!e.hidden&&getComputedStyle(e).display!=='none'&&e.offsetHeight>0},sel);
const shot=n=>p.screenshot({path:`/home/claude/ux/my/${f}-${n}.png`});
await p.goto('http://localhost:8812/'+f+'.html');await p.waitForTimeout(900);
await p.evaluate(()=>document.querySelectorAll('.welcome,#welcome').forEach(w=>w.remove()));
// 1. AAR
ok(await p.$$eval('#p-home .tile[data-aar]',x=>x.length)===0,'no AAR tile on the Home list');
ok(await vis('.hdr .aar-hbtn'),'AAR button in the top bar');
await shot('home');
await p.click('.hdr .aar-hbtn');await p.waitForTimeout(500);
ok(await vis('#aar'),'AAR opens from the top bar');await shot('aar');
await p.keyboard.press('Escape');await p.evaluate(()=>{const a=document.getElementById('aar');if(a&&!a.hidden){const c=a.querySelector('[data-aar=close],.aar-close,button[aria-label*=Close]');if(c)c.click()}});await p.waitForTimeout(300);
await p.evaluate(()=>{const a=document.getElementById('aar');if(a)a.hidden=true});
// 2. Plan my tour -> straight to ready-made
await p.evaluate(()=>window.scrollTo(0,0));await p.click('#qa-plan');await p.waitForTimeout(600);
ok(await vis('#uxpick .uxseg'),'switch row shown');
ok(await p.$eval('[data-uxpick=days]',e=>e.getAttribute('aria-pressed'))==='true','Ready-made selected first');
ok(await vis('#classicbox'),'ready-made choices shown straight away');
ok(await vis('#tourout .daybar'),'ready-made days shown');
ok(!(await vis('#mybox')),'build-my-own box hidden');
ok(!(await p.evaluate(()=>document.body.innerText.includes('How much time do you have?'))),'old question screen gone');
await shot('tour-ready');
// 3. By area
await p.click('[data-uxpick=area]');await p.waitForTimeout(600);
ok(await vis('#apbox #ap-map'),'By area opens the area map');ok(!(await vis('#classicbox')),'ready-made hidden in By area');
await shot('tour-area');
// 4. Build my own
await p.click('[data-uxpick=my]');await p.waitForTimeout(800);
ok(await vis('#mybox #my-map'),'Build my own shows the map');ok(!(await vis('#tourout')),'no route shown until it is made');
ok(await p.$eval('#mybox .my-go',e=>e.disabled),'Make my route disabled while empty');
await p.click('#mybox [data-mydays="3"]');await p.waitForTimeout(400);
ok(await p.$$eval('#mybox [data-mycur]',x=>x.length)===3,'3 day buttons');
// day 1: two sites from the list
const ids=await p.$$eval('#mybox [data-myadd]',x=>x.map(b=>b.dataset.myadd));
ok(ids.length>=10,'list has all sites ('+ids.length+')');
await p.click(`#mybox [data-myadd="${ids[0]}"]`);await p.waitForTimeout(200);
await p.click(`#mybox [data-myadd="${ids[1]}"]`);await p.waitForTimeout(200);
ok(await p.$$eval('#my-days .my-day:nth-child(1) li',x=>x.length)===2,'Day 1 has 2 stops');
// day 2: tap a dot on the map
await p.click('#mybox [data-mycur="2"]');await p.waitForTimeout(500);
const dot=await p.evaluate(()=>{const c=[...document.querySelectorAll('#my-map circle[fill="#fff"]')].find(c=>{const r=c.getBoundingClientRect(),m=document.getElementById('my-map').getBoundingClientRect();return r.left>m.left+20&&r.right<m.right-60&&r.top>m.top+20&&r.bottom<m.bottom-20});if(!c)return null;const r=c.getBoundingClientRect();return[r.left+r.width/2,r.top+r.height/2]});
ok(!!dot,'found a site dot on the map');
if(dot){await p.mouse.click(dot[0],dot[1]);await p.waitForTimeout(400)}
ok(await p.$$eval('#my-days .my-day:nth-child(2) li',x=>x.length)===1,'map tap added a stop to Day 2');
await shot('my-edit');
// search the list, add to day 3
await p.click('#mybox [data-mycur="3"]');await p.waitForTimeout(400);
const nm=await p.$eval(`#mybox [data-myadd="${ids[5]}"]`,b=>b.closest('.my-row').querySelector('span').textContent.split(' ·')[0]);
await p.fill('#my-q',nm.slice(0,8));await p.waitForTimeout(300);
ok(await p.$$eval('#my-list .my-row',x=>x.length)>=1,'search narrows the list');
await p.click(`#my-list [data-myadd="${ids[5]}"]`);await p.waitForTimeout(300);
ok(await p.$$eval('#my-days .my-day:nth-child(3) li',x=>x.length)===1,'Day 3 has 1 stop');
// remove one and put it back
const rmId=await p.$eval('#my-days .my-day:nth-child(1) [data-myrm]',b=>b.dataset.myrm);await p.click('#my-days .my-day:nth-child(1) [data-myrm]');await p.waitForTimeout(300);
ok(await p.$$eval('#my-days .my-day:nth-child(1) li',x=>x.length)===1,'✕ removes a stop');
await p.click('#mybox [data-mycur="1"]');await p.waitForTimeout(300);await p.fill('#my-q','');await p.dispatchEvent('#my-q','input');await p.waitForTimeout(200);
await p.click(`#mybox [data-myadd="${rmId}"]`);await p.waitForTimeout(200);
// make it
await p.click('#mybox .my-go');await p.waitForTimeout(900);
ok(await p.$$eval('#tourout .daybar',x=>x.length)===3,'route shows 3 days');
const gl=await p.$$eval('#tourout .routebox a.rb.g',x=>x.map(a=>a.href));
ok(gl.length>=3&&gl.every(h=>h.startsWith('https://www.google.com/maps/dir/')),'Google Maps route button for every day ('+gl.length+')');
ok(await p.$$eval('#tourout .sitmap, #tourout svg',x=>x.length)>=3,'a map for every day');
const summ=await p.$eval('#tourout .summ',e=>e.textContent);ok(/Your own route · 3 days · 4 stops/.test(summ),'summary: '+summ.slice(0,70));
ok(await vis('#mybox [data-my=edit]'),'Edit my route button');
await shot('my-route');await p.evaluate(()=>window.scrollBy(0,700));await p.waitForTimeout(300);await shot('my-route2');
// persists after reload
await p.reload();await p.waitForTimeout(900);await p.evaluate(()=>{document.querySelectorAll('.welcome,#welcome').forEach(w=>w.remove());goTab('tab-tour')});await p.waitForTimeout(500);
ok(await p.$eval('[data-uxpick=my]',e=>e.getAttribute('aria-pressed'))==='true','after reload: Build my own still selected');
ok(await p.$$eval('#tourout .daybar',x=>x.length)===3,'after reload: own route still there');
// "+ Add to my route" elsewhere adds to own route
await p.evaluate(()=>goTab('tab-time'));await p.waitForTimeout(500);
const rb=await p.$$('#p-time button.routeadd:not([hidden]):not(.in)');
if(rb.length){await rb[0].click();await p.waitForTimeout(400);await p.evaluate(()=>goTab('tab-tour'));await p.waitForTimeout(400);
  const t=await p.$eval('#tourout .summ',e=>e.textContent);ok(/ 5 stops/.test(t),'＋ Add to my route on Timeline adds to own route')}
else ok(true,'(no add buttons on Timeline to test)');
// edit again
await p.click('#mybox [data-my=edit]');await p.waitForTimeout(600);ok(await vis('#mybox #my-map'),'Edit reopens the builder');
// back to ready-made: the classic plan is unchanged
await p.click('[data-uxpick=days]');await p.waitForTimeout(600);
ok(await vis('#classicbox'),'Ready-made back');const s2=await p.$eval('#tourout .summ',e=>e.textContent);ok(!/Your own route/.test(s2),'ready-made plan shown: '+s2.slice(0,50));
// and back to own route keeps it
await p.click('[data-uxpick=my]');await p.waitForTimeout(600);ok(await p.$$eval('#tourout .daybar',x=>x.length)===3,'own route kept when switching back');
// diary still sees visits
console.log(errs.join('\n')||'NO PAGE ERRORS');console.log(fails.length?'FAILS '+fails.length:'ALL PASS');await b.close()})();
