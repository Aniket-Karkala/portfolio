(() => {
const root = document.documentElement;
root.classList.remove('no-js');
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
const fine = matchMedia('(pointer: fine)').matches;
const lerp = (a, b, t) => a + (b - a) * t;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const $ = (s, el = document) => el.querySelector(s), $$ = (s, el = document) => [...el.querySelectorAll(s)];
const ptr = { x: innerWidth / 2, y: innerHeight / 2, active: false };
addEventListener('pointermove', e => { ptr.x = e.clientX; ptr.y = e.clientY; ptr.active = true; }, { passive: true });
document.addEventListener('pointerleave', () => { ptr.active = false; });

/* ============ common: progress bar, pointer glow, scroll-linked bits ============ */
(function common() {
  const bar = $('.bar'), band = $('.parts-band'), xp = $('#xp'), glow = $('.glow'), stack = $('.stack');
  let tick = false, lastY = scrollY, vel = 0, bt;
  function update() {
    tick = false;
    const max = root.scrollHeight - innerHeight;
    if (bar) bar.style.setProperty('--p', max > 0 ? (scrollY / max).toFixed(4) : 0);
    if (band && !still) { vel = lerp(vel, (scrollY - lastY) * .06, .4); band.style.setProperty('--v', clamp(vel, -2.5, 2.5).toFixed(2)); clearTimeout(bt); bt = setTimeout(() => band.style.setProperty('--v', 0), 140); }
    lastY = scrollY;
    if (xp) { const r = xp.getBoundingClientRect(); xp.style.setProperty('--xp', clamp((innerHeight * .75 - r.top) / r.height, 0, 1).toFixed(3)); }
    if (stack && !still) stack.style.setProperty('--sway', (scrollY * .05).toFixed(1) + 'deg');
  }
  addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(update); } }, { passive: true });
  addEventListener('resize', update); update();
  if (glow && fine && !still) {
    let gx = ptr.x, gy = ptr.y;
    (function follow() { gx = lerp(gx, ptr.x, .08); gy = lerp(gy, ptr.y, .08); glow.style.transform = `translate(${gx.toFixed(1)}px,${gy.toFixed(1)}px)`; glow.classList.toggle('on', ptr.active); requestAnimationFrame(follow); })();
  }
})();

/* ============ headings fold up out of blur, blocks come into focus ============ */
(function reveal() {
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .15, rootMargin: '0px 0px -6% 0px' });
  $$('.sec-head').forEach(h => {
    const text = h.textContent; h.setAttribute('aria-label', text); h.textContent = ''; let i = 0;
    text.split(' ').forEach((word, wi, arr) => {
      const w = document.createElement('span'); w.className = 'w'; w.setAttribute('aria-hidden', 'true');
      [...word].forEach(ch => { const c = document.createElement('span'); c.className = 'c'; c.style.setProperty('--i', i++); c.textContent = ch; w.appendChild(c); });
      h.appendChild(w); if (wi < arr.length - 1) h.appendChild(document.createTextNode(' '));
    });
    io.observe(h);
  });
  $$('[data-r]').forEach(el => io.observe(el));
})();

/* ============ home hero: the name as a 3D point cloud with depth of field ============ */
(function hero3d() {
  const cv = $('#space'); if (!cv) return;
  const ctx = cv.getContext('2d'), hero = cv.parentElement;
  let W, H, pts = [], dust = [], halfW = 0, halfH = 0, running = false, visible = true, t0 = 0, yaw = 0, pitch = 0, cx, cy;
  const F = 950;
  function build() {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cx = W / 2; cy = H * .44;
    const off = document.createElement('canvas'); off.width = W; off.height = H;
    const o = off.getContext('2d', { willReadFrequently: true });
    const lines = ['Aniket', 'Karkala']; let fs = 400;
    const setFont = () => { o.font = `800 ${fs}px Bricolage, "Arial Narrow", sans-serif`; try { o.letterSpacing = (-fs * .035) + 'px'; } catch (e) {} };
    setFont();
    const widest = Math.max(...lines.map(l => o.measureText(l).width));
    fs = Math.min(fs * (W * .8) / widest, (H * .5) / (lines.length * .84)); setFont();
    o.fillStyle = '#fff'; o.textAlign = 'center'; o.textBaseline = 'alphabetic';
    const lh = fs * .84, top = cy - lh * lines.length / 2;
    lines.forEach((l, i) => o.fillText(l, cx, top + lh * (i + 1) - fs * .1));
    const data = o.getImageData(0, 0, W, H).data;
    let gap = Math.max(3, Math.round(fs / 44)), found;
    do { found = []; for (let y = 0; y < H; y += gap) for (let x = 0; x < W; x += gap) if (data[(y * W + x) * 4 + 3] > 128) found.push(x, y); gap++; } while (found.length / 2 > 6500);
    const depth = fs * .075, size = Math.max(1.8, (gap - 1) * .58);
    pts = []; halfW = 0; halfH = 0;
    for (let i = 0; i < found.length; i += 2) {
      const hx = found[i] - cx, hy = found[i + 1] - cy, hz = (((Math.random() * 3) | 0) - 1) * depth;
      halfW = Math.max(halfW, Math.abs(hx)); halfH = Math.max(halfH, Math.abs(hy));
      const a = Math.random() * 6.283, b = Math.acos(Math.random() * 2 - 1), r = 700 + Math.random() * 900;
      pts.push({ hx, hy, hz, x: still ? hx : r * Math.sin(b) * Math.cos(a), y: still ? hy : r * Math.cos(b), z: still ? hz : r * Math.sin(b) * Math.sin(a), ox: 0, oy: 0, b: .8, s: size, d: Math.random() * .9 + (hx + halfW) * .0006 });
    }
    dust = [];
    for (let i = 0; i < 230; i++) dust.push({ x: (Math.random() * 2 - 1) * W * .9, y: (Math.random() * 2 - 1) * H * .8, z: (Math.random() * 2 - 1) * 1100, v: .08 + Math.random() * .25, g: Math.random() < .22 });
    t0 = performance.now();
  }
  function frame(now) {
    if (!running) return;
    const t = (now - t0) / 1000;
    ctx.clearRect(0, 0, W, H);
    const r = hero.getBoundingClientRect(), mx = ptr.x - r.left, my = ptr.y - r.top;
    const inside = ptr.active && fine && my > 0 && my < H;
    const ty = still ? 0 : Math.sin(t * .35) * .16 + (inside ? (mx / W - .5) * .55 : 0);
    const tp = still ? 0 : Math.sin(t * .27) * .06 + (inside ? (my / H - .5) * -.45 : 0);
    yaw = lerp(yaw, ty, .05); pitch = lerp(pitch, tp, .05);
    const cyw = Math.cos(yaw), syw = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
    const proj = (x, y, z) => { const x1 = x * cyw + z * syw, z1 = -x * syw + z * cyw, y1 = y * cp - z1 * sp, z2 = y * sp + z1 * cp, s = F / (F + z2); return [cx + x1 * s, cy + y1 * s, s, z2]; };
    ctx.globalCompositeOperation = 'lighter';
    // out-of-focus dust: big soft discs far from the focal plane
    for (const d of dust) {
      if (!still) { d.y -= d.v; if (d.y < -H * .8) d.y = H * .8; }
      const [sx, sy, s, z] = proj(d.x, d.y, d.z); if (s <= 0) continue;
      const coc = Math.abs(z) * .012 + 1.2, rad = Math.min(20, coc * s);
      ctx.fillStyle = d.g ? `rgba(233,185,73,${(.5 / (coc * coc * .12 + 1.4)).toFixed(3)})` : `rgba(124,86,201,${(.75 / (coc * coc * .1 + 1.3)).toFixed(3)})`;
      ctx.beginPath(); ctx.arc(sx, sy, rad, 0, 6.283); ctx.fill();
    }
    // scan plane sweeps through the cloud
    const period = 6.5, ph = ((t - 2.4) % period + period) % period;
    const scanX = t < 2.4 || still ? -1e6 : lerp(-halfW - 90, halfW + 90, Math.min(1, ph / 3.4));
    const scanning = ph < 3.4 && t >= 2.4 && !still;
    if (scanning) {
      const dz = 260, hh = halfH * 1.35, q = [proj(scanX, -hh, -dz), proj(scanX, -hh, dz), proj(scanX, hh, dz), proj(scanX, hh, -dz)];
      ctx.fillStyle = 'rgba(233,185,73,.07)'; ctx.strokeStyle = 'rgba(233,185,73,.55)'; ctx.lineWidth = 1.2;
      ctx.beginPath(); q.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.closePath(); ctx.fill(); ctx.stroke();
    }
    let lastK = -1;
    for (let i = 0; i < pts.length; i++) {
      const p = pts[i];
      if (!still && t > p.d) { p.x += (p.hx - p.x) * .07; p.y += (p.hy - p.y) * .07; p.z += (p.hz - p.z) * .07; }
      if (scanning && Math.abs(p.hx - scanX) < 14) p.b = 1; else if (p.b > .8) p.b += (.8 - p.b) * .03;
      const [sx0, sy0, s, z] = proj(p.x + p.ox, p.y + p.oy, p.z); if (s <= 0 || s > 6) continue;
      if (inside) { const dx = sx0 - mx, dy = sy0 - my, d2 = dx * dx + dy * dy; if (d2 < 8100) { const d = Math.sqrt(d2) || 1, f = (1 - d / 90) * 4; p.ox += dx / d * f; p.oy += dy / d * f; p.b = Math.max(p.b, .92); } }
      p.ox *= .9; p.oy *= .9;
      const coc = 1 + Math.abs(z) * .006, sz = p.s * s * coc, al = p.b / (coc * coc);
      const k = (p.b > .86 ? 100 : 0) + Math.min(20, (al * 20) | 0);
      if (k !== lastK) { ctx.fillStyle = k >= 100 ? `rgba(233,185,73,${(Math.min(1, (k - 100) / 16)).toFixed(2)})` : `rgba(226,214,250,${(k / 20).toFixed(2)})`; lastK = k; }
      ctx.fillRect(sx0 - sz / 2, sy0 - sz / 2, sz, sz);
    }
    ctx.globalCompositeOperation = 'source-over';
    if (still) { running = false; return; }
    requestAnimationFrame(frame);
  }
  const start = () => { if (!running && visible) { running = true; requestAnimationFrame(frame); } };
  const ready = () => { build(); start(); };
  (document.fonts && document.fonts.load ? document.fonts.load('800 100px Bricolage').catch(() => {}) : Promise.resolve()).then(ready);
  let rt, lastW = innerWidth;
  addEventListener('resize', () => { if (innerWidth === lastW) return; lastW = innerWidth; clearTimeout(rt); rt = setTimeout(ready, 180); });
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) start(); else running = false; }).observe(hero);
})();

/* ============ featured projects on a 3D ring; cards off-centre fall out of focus ============ */
(function coverflow() {
  const cf = $('.cf'); if (!cf) return;
  const ring = $('.ring', cf), cards = $$('.cf-card', cf), n = cards.length, step = 360 / n, label = $('#cf-n');
  let a = 0, target = 0, R = 0, dragging = false, sx = 0, sa = 0, moved = 0, auto, on = false, hover = false;
  function size() { const cw = parseFloat(getComputedStyle(cf).getPropertyValue('--cw')); R = Math.round(cw / 2 / Math.tan(Math.PI / n)) + 46; cards.forEach((c, i) => { c.style.transform = `rotateY(${i * step}deg) translateZ(${R}px)`; }); }
  function draw() {
    if (!on) return;
    if (!dragging) a = still ? target : lerp(a, target, .09);
    ring.style.transform = `translateZ(${-R}px) rotateY(${(-a).toFixed(2)}deg)`;
    cards.forEach((c, i) => {
      let d = ((i * step - a) % 360 + 540) % 360 - 180; const ad = Math.abs(d);
      c.style.filter = ad < 4 ? 'none' : `blur(${Math.min(7, ad / step * 2.2).toFixed(1)}px)`;
      c.style.opacity = ad > 115 ? 0 : (1 - ad / 150).toFixed(2);
      c.style.pointerEvents = ad < step * .6 ? 'auto' : 'none';
      c.classList.toggle('front', ad < step / 2); c.tabIndex = ad < step / 2 ? 0 : -1;
    });
    if (label) label.textContent = (((Math.round(target / step) % n) + n) % n + 1) + ' / ' + n;
    requestAnimationFrame(draw);
  }
  const go = d => { target = Math.round(target / step) * step + d * step; };
  $('#cf-prev').addEventListener('click', () => go(-1)); $('#cf-next').addEventListener('click', () => go(1));
  cf.addEventListener('pointerdown', e => { dragging = true; moved = 0; sx = e.clientX; sa = a; cf.classList.add('drag'); });
  addEventListener('pointermove', e => { if (!dragging) return; const dx = e.clientX - sx; moved = Math.max(moved, Math.abs(dx)); a = sa - dx * .22; });
  addEventListener('pointerup', () => { if (!dragging) return; dragging = false; cf.classList.remove('drag'); target = Math.round(a / step) * step; });
  cf.addEventListener('click', e => { if (moved > 8) e.preventDefault(); }, true);
  cf.addEventListener('dragstart', e => e.preventDefault());
  cf.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') go(-1); if (e.key === 'ArrowRight') go(1); });
  cf.parentElement.addEventListener('pointerenter', () => hover = true); cf.parentElement.addEventListener('pointerleave', () => hover = false);
  size(); addEventListener('resize', size);
  new IntersectionObserver(([e]) => { const was = on; on = e.isIntersecting; if (on && !was) requestAnimationFrame(draw); clearInterval(auto); if (on && !still) auto = setInterval(() => { if (!hover && !dragging && !document.hidden) go(1); }, 3800); }).observe(cf);
})();

/* ============ projects index: filter by type, size and text ============ */
(function index() {
  const grid = $('#grid'); if (!grid) return;
  const cards = $$('.card', grid), count = $('#count'), empty = $('#empty'), search = $('#q');
  const state = { cat: 'all', scale: 'all', q: '' };
  const qs = new URLSearchParams(location.search);
  if (qs.get('scale')) state.scale = qs.get('scale'); if (qs.get('cat')) state.cat = qs.get('cat');
  function apply() {
    let n = 0;
    cards.forEach(c => { const ok = (state.cat === 'all' || c.dataset.cat === state.cat) && (state.scale === 'all' || c.dataset.scale === state.scale) && (!state.q || c.dataset.text.includes(state.q)); c.hidden = !ok; if (ok) n++; });
    count.textContent = n + (n === 1 ? ' project' : ' projects'); empty.hidden = n > 0;
    $$('.chip').forEach(ch => ch.setAttribute('aria-pressed', String(state[ch.dataset.k] === ch.dataset.v)));
  }
  const run = () => (document.startViewTransition && !still) ? document.startViewTransition(apply) : apply();
  $$('.chip').forEach(ch => ch.addEventListener('click', () => { state[ch.dataset.k] = ch.dataset.v; run(); }));
  search.addEventListener('input', () => { state.q = search.value.trim().toLowerCase(); apply(); });
  apply();
})();

/* ============ project page: exploded stack ============ */
(function stack() {
  const st = $('.stack'); if (!st) return;
  setTimeout(() => st.classList.add('ready'), still ? 0 : 450);
  $$('.flow>div').forEach((d, i) => { d.addEventListener('pointerenter', () => st.dataset.focus = i); d.addEventListener('pointerleave', () => delete st.dataset.focus); });
  if (fine && !still) st.addEventListener('pointermove', e => { const r = st.getBoundingClientRect(); st.style.setProperty('--sway', (((e.clientX - r.left) / r.width - .5) * 50 + scrollY * .05).toFixed(1) + 'deg'); });
})();

/* ============ 8x8 time-of-flight grid ============ */
(function tof() {
  const el = $('#tof'); if (!el) return; const cells = [];
  for (let i = 0; i < 64; i++) { const c = document.createElement('i'); el.appendChild(c); cells.push(c); }
  let on = false, t = 0;
  function draw() {
    if (!on) return;
    const r = el.getBoundingClientRect(); t += .012;
    const usePtr = ptr.active && fine && !still;
    const px = usePtr ? ptr.x : r.left + r.width * (.5 + .34 * Math.sin(t * 1.3)), py = usePtr ? ptr.y : r.top + r.height * (.5 + .34 * Math.cos(t * .9));
    const reach = usePtr ? Math.max(r.width * 1.1, 360) : r.width * .62;
    cells.forEach((c, i) => {
      const cx = r.left + (i % 8 + .5) * r.width / 8, cy = r.top + ((i >> 3) + .5) * r.height / 8;
      const n = Math.max(0, 1 - Math.hypot(cx - px, cy - py) / reach), k = n * n;
      c.style.background = k > .45 ? '#E9B949' : k > .16 ? '#B98FE8' : '#7C56C9';
      c.style.opacity = (.22 + .78 * k).toFixed(2); c.style.transform = `scale(${(.82 + .18 * k).toFixed(2)})`;
    });
    if (!still) requestAnimationFrame(draw); else on = false;
  }
  new IntersectionObserver(([e]) => { const was = on; on = e.isIntersecting; if (on && !was) requestAnimationFrame(draw); }).observe(el);
})();

/* ============ count-up, tilt, magnets, card light ============ */
(function bits() {
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return; io.unobserve(e.target);
    const el = e.target, n = +el.dataset.n; if (still) return;
    const t0 = performance.now(), dur = 1200;
    (function stepf(now) { const k = Math.min(1, (now - t0) / dur); el.textContent = Math.round(n * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(stepf); })(t0);
  }), { threshold: .6 });
  $$('[data-n]').forEach(el => io.observe(el));
  if (!fine || still) return;
  $$('.tilt').forEach(el => {
    el.addEventListener('pointermove', e => { const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height; el.style.setProperty('--mx', (x * 100).toFixed(0) + '%'); el.style.setProperty('--my', (y * 100).toFixed(0) + '%'); el.style.transform = `perspective(900px) rotateX(${((.5 - y) * 9).toFixed(2)}deg) rotateY(${((x - .5) * 11).toFixed(2)}deg) translateZ(14px)`; });
    el.addEventListener('pointerleave', () => { el.style.transform = ''; });
  });
  $$('.magnet').forEach(el => {
    el.addEventListener('pointermove', e => { const r = el.getBoundingClientRect(); el.style.transform = `translate(${((e.clientX - r.left - r.width / 2) * .28).toFixed(1)}px,${((e.clientY - r.top - r.height / 2) * .4).toFixed(1)}px)`; });
    el.addEventListener('pointerleave', () => { el.style.transition = 'transform .5s cubic-bezier(.2,.8,.2,1),background .25s,color .25s,border-color .25s'; el.style.transform = ''; setTimeout(() => el.style.transition = '', 500); });
  });
})();

/* ============ footer: oscilloscope trace ============ */
(function scope() {
  const cv = $('#scope'); if (!cv) return; const ctx = cv.getContext('2d');
  let W, H, on = false, t = 0, freq = 3, amp = .5;
  function size() { const d = Math.min(devicePixelRatio || 1, 2); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * d; cv.height = H * d; ctx.setTransform(d, 0, 0, d, 0, 0); }
  function draw() {
    if (!on) return;
    const r = cv.getBoundingClientRect(), near = ptr.active && fine && ptr.y > r.top - 260;
    freq = lerp(freq, near ? 2 + (ptr.x / innerWidth) * 9 : 3, .05); amp = lerp(amp, near ? .95 : .5, .05); t += .035;
    ctx.clearRect(0, 0, W, H);
    for (let pass = 0; pass < 2; pass++) {
      ctx.beginPath();
      for (let x = 0; x <= W; x += 3) { const u = x / W, env = Math.sin(u * Math.PI); const y = H / 2 + Math.sin(u * freq * Math.PI * 2 - t * (pass ? 1.6 : 1)) * H * .36 * amp * env * (pass ? .55 : 1) + Math.sin(u * 37 + t * 3) * 1.5; x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
      ctx.strokeStyle = pass ? 'rgba(124,86,201,.8)' : '#E9B949'; ctx.lineWidth = pass ? 1.5 : 2.5; ctx.stroke();
    }
    if (!still) requestAnimationFrame(draw); else on = false;
  }
  size(); addEventListener('resize', () => { size(); if (still) { on = true; draw(); } });
  new IntersectionObserver(([e]) => { const was = on; on = e.isIntersecting; if (on && !was) requestAnimationFrame(draw); }).observe(cv);
})();
})();
