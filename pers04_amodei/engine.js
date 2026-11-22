// Reusable engine for "Lo sapevi? Te lo spiega Claudio" reels.
// A page defines: window.ORDER (section ids), window.DURS (voice seconds per id), R[id](lt, d) scene renderers,
// and markup with <div class="scene" id="<id>">. The intro scene "I" is provided here.
const $ = id => document.getElementById(id);
const cl = x => Math.max(0, Math.min(1, x));
const P = (t, a, b) => cl((t - a) / (b - a));
const eo = x => 1 - Math.pow(1 - x, 3), eio = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const eback = x => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2) };
const ex = x => x === 1 ? 1 : 1 - Math.pow(2, -10 * x);
function rnd(s) { let x = Math.sin(s * 12.9898) * 43758.5453; return x - Math.floor(x) }
const fmt = (v, d = 0) => v.toFixed(d).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.');

function ap(el, t, t0, d = .35, dy = 40, sc = 1, base = 'translateX(-50%)') {
  const k = eo(P(t, t0, t0 + d)); el.style.opacity = k; el.style.filter = `blur(${(1 - k) * 14}px)`;
  el.style.transform = `${base} translateY(${(1 - k) * dy}px) scale(${sc + (1 - sc) * k})`;
}
function pop(el, t, t0, d = .45, rot = 0, final = 0, base = 'translateX(-50%)') {
  const k = P(t, t0, t0 + d), e = eback(k); el.style.opacity = cl(k * 4); el.style.filter = `blur(${(1 - cl(k * 3)) * 10}px)`;
  el.style.transform = `${base} scale(${.2 + .8 * e}) rotate(${rot * (1 - e) + final}deg)`;
}
const wcache = {};
function words(el, t, t0, per = .09) {
  if (!wcache[el.id]) { wcache[el.id] = 1; el.innerHTML = el.innerHTML.split(/(<span[^>]*>.*?<\/span>|\s+)/).filter(s => s && !/^\s+$/.test(s)).map(w => `<span class="w">${w}</span>`).join('') }
  el.style.transform = 'translateX(-50%)';
  [...el.children].forEach((w, i) => { const k = eo(P(t, t0 + i * per, t0 + i * per + .35)); w.style.opacity = k; w.style.filter = `blur(${(1 - k) * 12}px)`; w.style.transform = `translateY(${(1 - k) * 24}px)` })
}
function typeT(el, txt, t, t0, cps = 26) { const n = Math.floor(Math.max(0, t - t0) * cps); el.innerHTML = txt.slice(0, n) + (n < txt.length && t >= t0 ? '<span style="opacity:' + (Math.floor(t * 3) % 2) + '">▍</span>' : '') }
function drawPath(el, t, a, b) { const L = el.getTotalLength(); el.style.strokeDasharray = L; el.style.strokeDashoffset = L * (1 - eio(P(t, a, b))) }

// ---- series signature intro ----
const INTRO_HTML = `<div class="scene" id="I" style="background:var(--dark)">
 <div class="abs bold" id="Ia" style="top:700px;font-size:150px;color:#fff">LO SAPEVI?</div>
 <div class="abs serif" id="Ib" style="top:900px;font-size:76px;color:#bdb3a6">te lo spiega</div>
 <div class="abs serif" id="Ic" style="top:975px;font-size:150px;color:var(--orange)">Claudio</div>
 <svg width="1080" height="1920" style="position:absolute;inset:0;overflow:visible"><path id="Iu" d="M330 1150 C 450 1128, 640 1122, 760 1136 C 800 1141, 790 1156, 740 1158" stroke="#e2683c" stroke-width="7" fill="none" stroke-linecap="round"/></svg></div>`;
const R = {};
R.I = lt => { pop($('Ia'), lt, .05, .4, -6); words($('Ib'), lt, .85, .1); pop($('Ic'), lt, 1.3, .45, 4); drawPath($('Iu'), lt, 1.55, 2.0) };

// ---- voice-driven timing ----
const LEAD = .35, GAP = .45, PRE = .25, TAIL = 1.6;
function buildTiming() {
  const W = {}, starts = {}; let t = LEAD;
  ORDER.forEach((k, i) => { starts[k] = t; W[k] = [i === 0 ? 0 : t - PRE, null]; t += DURS[k] + GAP });
  ORDER.forEach((k, i) => { W[k][1] = i + 1 < ORDER.length ? W[ORDER[i + 1]][0] : starts[k] + DURS[k] + TAIL });
  return { W, starts, dur: W[ORDER[ORDER.length - 1]][1] };
}
let TM;
window.render = function (t) {
  ORDER.forEach(id => {
    const el = $(id), [a, b] = TM.W[id];
    if (t >= a && t < b) {
      el.style.display = 'block'; const lt = t - a, d = b - a, last = id === ORDER[ORDER.length - 1];
      const kin = eo(P(lt, 0, .18)), kout = P(lt, d - .14, d);
      el.style.filter = `blur(${(1 - kin) * 16 + (last ? 0 : kout * 18)}px)`;
      el.style.transform = `scale(${1.06 - .06 * kin + (last ? 0 : kout * .08)}) translateY(${last ? 0 : kout * -40}px)`;
      R[id](lt, d); if (last) el.style.opacity = 1 - P(lt, d - .5, d);
    } else el.style.display = 'none';
  });
  if (window.afterRender) window.afterRender(t);
};
window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('stage').insertAdjacentHTML('afterbegin', INTRO_HTML);
  TM = buildTiming(); window.DUR = TM.dur; window.TIMING = TM;
});
window.ready = new Promise(r => window.addEventListener('load', () => document.fonts.ready.then(() => { render(0); r(true) })));
