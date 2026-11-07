/* Heidi Gubbins — motion & navigation runtime
   - Smooth scroll (Lenis, progressive)
   - First-visit loader
   - PJAX page transitions with curtain
   - Split-text, image and fade reveals on view
   - Parallax, pinned horizontal scroller, header states, progress
   - Menu, cursor, project filters/list hover preview, lightbox, forms */
(() => {
  const html = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));

  /* ---------- Smooth scroll ---------- */
  let lenis = null;
  if (window.Lenis && !reduce) {
    lenis = new Lenis({ duration: 1.15, easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true });
    const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }
  const scrollTop = () => (lenis ? lenis.scrollTo(0, { immediate: true, force: true }) : window.scrollTo(0, 0));

  /* ---------- Split text ---------- */
  function split(el) {
    if (el.dataset.splitDone) return;
    let i = 0;
    const walk = (node) => {
      [...node.childNodes].forEach((n) => {
        if (n.nodeType === 3) {
          const parts = n.textContent.split(/(\s+)/);
          const frag = document.createDocumentFragment();
          parts.forEach((p) => {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(' ')); return; }
            const w = document.createElement('span'); w.className = 'w';
            const s = document.createElement('span'); s.style.setProperty('--i', i++); s.textContent = p;
            w.appendChild(s); frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
      });
    };
    walk(el);
    el.style.setProperty('--step', i > 14 ? '.018s' : '.05s');
    el.classList.add('split');
    el.dataset.splitDone = '1';
  }

  /* ---------- Reveal observer ---------- */
  let io;
  function observe(scope) {
    io && io.disconnect();
    io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const t = e.target;
        t.classList.add('is-in');
        if (t.dataset.count) countUp(t);
        io.unobserve(t);
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0 });
    $$('[data-split],[data-reveal],[data-img],[data-line],[data-count]', scope).forEach((el) => io.observe(el));
    // safety net: anything already on screen reveals immediately
    requestAnimationFrame(() => $$('[data-split],[data-reveal],[data-img],[data-line]', scope).forEach((el) => {
      const r = el.getBoundingClientRect(); if (r.top < innerHeight && r.bottom > 0) el.classList.add('is-in');
    }));
  }
  function countUp(el) {
    const end = +el.dataset.count; const dur = 1800; const t0 = performance.now();
    const step = (t) => { const p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 4))) + (el.dataset.suffix || ''); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  }

  /* ---------- Scroll-driven loop ---------- */
  let parallax = [], hscrolls = [], lastY = 0, header, progress, darkHero;
  function measure() {
    parallax = $$('[data-speed]').map((el) => ({ el, speed: +el.dataset.speed }));
    hscrolls = $$('.hscroll').map((sec) => {
      const track = $('.hscroll__track', sec);
      if (innerWidth < 900) { sec.style.height = ''; return null; }
      const dist = track.scrollWidth - innerWidth;
      sec.style.height = dist + innerHeight + 'px';
      return { sec, track, dist };
    }).filter(Boolean);
    darkHero = $('[data-header="light"]');
  }
  function tick() {
    const y = window.scrollY, vh = innerHeight;
    parallax.forEach(({ el, speed }) => {
      const r = el.parentElement.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      const off = (r.top + r.height / 2 - vh / 2) * speed;
      el.style.transform = `translate3d(0, ${off.toFixed(1)}px, 0)`;
    });
    hscrolls.forEach(({ sec, track, dist }) => {
      const top = sec.getBoundingClientRect().top;
      const p = Math.min(1, Math.max(0, -top / (sec.offsetHeight - vh)));
      track.style.transform = `translate3d(${(-p * dist).toFixed(1)}px,0,0)`;
    });
    const max = document.documentElement.scrollHeight - vh;
    progress && (progress.style.transform = `scaleX(${max > 0 ? y / max : 0})`);
    if (header && !html.classList.contains('is-menu-open')) {
      const overDark = darkHero && y < darkHero.offsetHeight - 80;
      header.classList.toggle('is-light', !!overDark);
      header.classList.toggle('is-solid', !overDark && y > 40);
      if (y > 400 && y > lastY + 4) header.classList.add('is-hidden');
      else if (y < lastY - 4 || y < 400) header.classList.remove('is-hidden');
    }
    lastY = y;
    requestAnimationFrame(tick);
  }

  /* ---------- Hero slideshow ---------- */
  let heroTimer;
  function hero(scope) {
    clearInterval(heroTimer);
    const root = $('.hero', scope); if (!root) return;
    const slides = $$('.hero__slide', root), caps = $$('.hero__caption span', root);
    const idx = $('[data-hero-idx]', root), bar = $('.hero__counter .bar i', root);
    let i = 0;
    const show = (n) => {
      slides.forEach((s, k) => s.classList.toggle('is-on', k === n));
      caps.forEach((c, k) => (c.style.transform = `translateY(${(k - n) * 100}%)`));
      idx && (idx.textContent = String(n + 1).padStart(2, '0'));
      if (bar) { bar.classList.remove('run'); void bar.offsetWidth; bar.classList.add('run'); }
    };
    show(0);
    if (slides.length > 1) heroTimer = setInterval(() => show((i = (i + 1) % slides.length)), 6000);
  }

  /* ---------- Projects: filter + view + floater ---------- */
  function projects(scope) {
    const root = $('[data-projects]', scope); if (!root) return;
    $$('.filter', root).forEach((f) => f.addEventListener('click', () => {
      const c = f.dataset.f;
      $$('.filter', root).forEach((x) => x.classList.toggle('is-active', x === f));
      $('.pgrid', root).classList.toggle('is-filtered', c !== 'all');
      $$('[data-cat]', root).forEach((el) => el.classList.toggle('is-hidden', c !== 'all' && el.dataset.cat !== c));
      $$('.pcard:not(.is-hidden) [data-img]', root).forEach((el) => el.classList.add('is-in'));
    }));
  }

  /* ---------- Lightbox ---------- */
  function lightbox(scope) {
    const lb = $('.lightbox'); if (!lb) return;
    const img = $('img', lb);
    $$('[data-zoom]', scope).forEach((el) => el.addEventListener('click', () => {
      img.src = $('img', el).currentSrc || $('img', el).src; img.alt = $('img', el).alt;
      lb.classList.add('is-open'); lenis && lenis.stop();
    }));
    const close = () => { lb.classList.remove('is-open'); lenis && lenis.start(); };
    lb.onclick = close; document.addEventListener('keydown', (e) => e.key === 'Escape' && close());
  }

  /* ---------- Forms ---------- */
  function forms(scope) {
    $$('form[data-mailto]', scope).forEach((f) => f.addEventListener('submit', (e) => {
      e.preventDefault();
      const d = new FormData(f);
      const body = [...d.entries()].filter(([k]) => !['subject', 'privacy'].includes(k)).map(([k, v]) => `${k[0].toUpperCase() + k.slice(1)}: ${v}`).join('\n');
      location.href = `mailto:${f.dataset.mailto}?subject=${encodeURIComponent(d.get('subject') || 'Website enquiry')}&body=${encodeURIComponent(body)}`;
      $('.form-note', f).textContent = 'Thank you — your email client will open to send your message.';
    }));
    $$('form[data-newsletter]', scope).forEach((f) => f.addEventListener('submit', (e) => {
      e.preventDefault(); $('.form-note', f).textContent = 'Thank you — you are on the list.'; f.reset();
    }));
  }

  /* ---------- Menu ---------- */
  function menu() {
    const btn = $('.menu-btn'); if (!btn) return;
    btn.addEventListener('click', () => {
      const open = html.classList.toggle('is-menu-open');
      btn.setAttribute('aria-expanded', open);
      $('.menu').setAttribute('aria-hidden', !open);
      lenis && (open ? lenis.stop() : lenis.start());
    });
    const imgs = $$('.menu__media img');
    $$('.menu__list a').forEach((a, k) => a.addEventListener('mouseenter', () => imgs.forEach((im, j) => im.classList.toggle('is-on', j === k))));
  }
  const closeMenu = () => { html.classList.remove('is-menu-open'); $('.menu-btn')?.setAttribute('aria-expanded', false); lenis && lenis.start(); };

  /* ---------- Cursor ---------- */
  function cursor() {
    if (!fine || reduce) return;
    html.classList.add('has-cursor');
    const c = $('.cursor'), label = $('.cursor__label');
    let x = innerWidth / 2, y = innerHeight / 2, cx = x, cy = y;
    addEventListener('mousemove', (e) => { x = e.clientX; y = e.clientY; });
    const loop = () => { cx += (x - cx) * 0.2; cy += (y - cy) * 0.2; c.style.transform = `translate3d(${cx}px,${cy}px,0)`; requestAnimationFrame(loop); };
    loop();
    document.addEventListener('mouseover', (e) => {
      const t = e.target.closest('[data-cursor]');
      const l = e.target.closest('a,button');
      c.classList.toggle('is-label', !!t);
      if (t) label.textContent = t.dataset.cursor;
      c.classList.toggle('is-link', !t && !!l);
    });
  }

  /* ---------- Page init ---------- */
  function initPage(scope = document) {
    $$('[data-split]', scope).forEach(split);
    measure();
    hero(scope); projects(scope); lightbox(scope); forms(scope);
    // active nav
    const path = location.pathname.replace(/index\.html$/, '');
    $$('[data-nav]').forEach((a) => {
      const href = new URL(a.href).pathname.replace(/index\.html$/, '');
      a.classList.toggle('is-active', href.length > 1 && path.startsWith(href));
    });
  }

  /* ---------- Router (PJAX + curtain) ---------- */
  let busy = false;
  const isInternal = (a) => a && a.href && a.origin === location.origin && !a.target && !a.hasAttribute('download') && !a.getAttribute('href').startsWith('#') && !/^(mailto|tel):/.test(a.getAttribute('href')) && location.protocol !== 'file:';
  async function go(url, { push = true, label = '' } = {}) {
    if (busy) return; busy = true;
    $('.curtain__label span').textContent = label || '';
    closeMenu();
    html.classList.remove('is-entering');
    html.classList.add('is-leaving');
    const [res] = await Promise.all([fetch(url).then((r) => r.text()).catch(() => null), wait(reduce ? 0 : 950)]);
    if (!res) { location.href = url; return; }
    const doc = new DOMParser().parseFromString(res, 'text/html');
    const next = doc.querySelector('#app');
    if (!next) { location.href = url; return; }
    if (push) history.pushState({}, '', url);
    document.title = doc.title;
    $('#app').replaceWith(next);
    header = $('.header'); menu();
    scrollTop();
    const hash = new URL(url, location.href).hash;
    initPage(next);
    html.classList.add('is-entering');
    html.classList.remove('is-leaving');
    await wait(250);
    observe(next);
    if (hash) { const t = $(hash); t && (lenis ? lenis.scrollTo(t, { offset: -80 }) : t.scrollIntoView()); }
    await wait(900);
    html.classList.remove('is-entering');
    busy = false;
  }
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (!isInternal(a) || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    const u = new URL(a.href);
    if (u.pathname === location.pathname && u.hash) return;
    e.preventDefault();
    if (u.href === location.href) { closeMenu(); return; }
    go(u.href, { label: a.dataset.label || '' });
  });
  addEventListener('popstate', () => go(location.href, { push: false }));
  history.scrollRestoration = 'manual';
  addEventListener('resize', () => { clearTimeout(window.__rz); window.__rz = setTimeout(measure, 150); });

  /* ---------- Boot ---------- */
  async function boot() {
    header = $('.header'); progress = $('.progress');
    menu(); cursor(); initPage();
    requestAnimationFrame(tick);
    const loader = $('.loader');
    let first = true; try { first = !sessionStorage.getItem('hg-v'); sessionStorage.setItem('hg-v', '1'); } catch (e) {}
    if (loader && first && !reduce) {
      const pct = $('.loader__pct'), line = $('.loader__line');
      const t0 = performance.now(), dur = 1700;
      await new Promise((res) => {
        const step = (t) => {
          const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
          pct.textContent = String(Math.round(e * 100)).padStart(3, '0');
          line.style.transform = `scaleX(${e})`;
          p < 1 ? requestAnimationFrame(step) : res();
        };
        requestAnimationFrame(step);
      });
      loader.classList.add('is-done');
      await wait(450);
      observe(document);
      setTimeout(() => loader.remove(), 1200);
    } else {
      loader && loader.remove();
      observe(document);
    }
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', boot) : boot();
})();
