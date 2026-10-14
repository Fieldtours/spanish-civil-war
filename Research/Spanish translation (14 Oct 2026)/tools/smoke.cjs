// Load an app page in jsdom, open every screen we can find, collect JS errors and visible English leftovers.
const { JSDOM, VirtualConsole } = require("/home/claude/pakmondo-rebuild/node_modules/jsdom");
const fs = require("fs");
const file = process.argv[2];
const html = fs.readFileSync(file, "utf8");
const errors = [];
const vc = new VirtualConsole();
vc.on("jsdomError", e => errors.push("jsdomError: " + (e.message || e).toString().slice(0, 200)));
vc.on("error", (...a) => errors.push("console.error: " + a.join(" ").slice(0, 200)));
const dom = new JSDOM(html, { url: "https://dzcharlie.com/spanish-civil-war/" + (file.endsWith("es.html") ? "es.html" : ""), runScripts: "dangerously", pretendToBeVisual: true, virtualConsole: vc,
  beforeParse(w) {
    w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (t, k) => k === "measureText" ? () => ({ width: 10 }) : (k === "canvas" ? {} : () => ({ addColorStop() {} })), set: () => true });
    w.matchMedia = () => ({ matches: false, addEventListener() {}, addListener() {} });
    w.scrollTo = () => {}; w.ResizeObserver = class { observe(){} unobserve(){} disconnect(){} };
    w.fetch = () => Promise.reject(new Error("offline"));
    w.Element.prototype.scrollIntoView = () => {};
  } });
const w = dom.window;
w.addEventListener("error", e => errors.push("error: " + e.message));
setTimeout(() => {
  const d = w.document;
  const go = d.getElementById("wel-go"); if (go) go.click();
  const seen = new Set(); let clicks = 0;
  const pass = () => {
    const btns = [...d.querySelectorAll("button, a[href^='#'], [data-go], [data-nav], .tile")].filter(b => !seen.has(b));
    for (const b of btns.slice(0, 400)) { seen.add(b); try { b.click(); clicks++; } catch (e) { errors.push("click: " + e.message); } }
  };
  pass(); setTimeout(() => { pass(); setTimeout(() => {
    const cl = d.body.cloneNode(true); cl.querySelectorAll("script,style").forEach(x=>x.remove()); const txt = cl.textContent.replace(/\s+/g, " ");
    if(process.argv[3]) fs.writeFileSync(process.argv[3], txt); console.log(JSON.stringify({ file, clicks, errors: [...new Set(errors)].slice(0, 30), length: txt.length, sample: txt.slice(0, 600) }, null, 1));
    process.exit(0);
  }, 400); }, 400);
}, 1500);
