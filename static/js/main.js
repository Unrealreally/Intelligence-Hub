/* ============================================================
   Intelligence Hub — main.js
   Vanilla JS UI enhancements.
   ============================================================= */

(function () {
  'use strict';

  /* ---------- Utils ---------- */
  const $ = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));

  const easeOutExpo = (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t));

  /* ---------- Animated counters ---------- */
  function animateCounter(el, to, duration = 1200) {
    if (isNaN(to)) return;
    const start = performance.now();
    const from = 0;
    const isFloat = String(to).indexOf('.') !== -1;
    function tick(now) {
      const p = Math.min(1, (now - start) / duration);
      const v = from + (to - from) * easeOutExpo(p);
      el.textContent = isFloat ? v.toFixed(1) : Math.round(v).toLocaleString();
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = isFloat ? Number(to).toFixed(1) : Number(to).toLocaleString();
    }
    requestAnimationFrame(tick);
  }

  function initCounters() {
    if (!('IntersectionObserver' in window)) return;
    const targets = $$('[data-counter]');

    if (!targets.length) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          const el = e.target;
          const raw = (el.getAttribute('data-counter') || el.textContent || '').replace(/[^\d.\-]/g, '');
          const to = parseFloat(raw);
          if (!isNaN(to)) animateCounter(el, to);
          io.unobserve(el);
        }
      });
    }, { threshold: 0.35 });
    targets.forEach((t) => io.observe(t));
  }

  /* ---------- Progress bars (dimension + feature) ---------- */
  function initBars() {
    if (!('IntersectionObserver' in window)) return;
    const bars = $$('[data-progress]');

    if (!bars.length) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          const el = e.target;
          const pct = Math.max(0, Math.min(100, parseFloat(el.getAttribute('data-progress')) || 0));
          requestAnimationFrame(() => { el.style.setProperty('--w', pct + '%'); });
          io.unobserve(el);
        }
      });
    }, { threshold: 0.3 });
    bars.forEach((b) => io.observe(b));
  }


  /* ---------- Signal Bars ---------- */

function initSignalBars(){

    const bars = document.querySelectorAll(".signal-fill");

    if(!bars.length) return;


    bars.forEach(bar=>{

        const value = Math.max(
            0,
            Math.min(
                100,
                Number(bar.dataset.value || 0)
            )
        );


        requestAnimationFrame(()=>{
            bar.style.width = value + "%";
        });

    });

}

  /* ---------- Score ring ---------- */

  function initScoreRing() {
    if (!('IntersectionObserver' in window)) return;
    const ring = $('.score-ring');

    if (!ring) return;
    const fill = ring.querySelector('.fill');
    const valEl = ring.querySelector('[data-score]');
    if (!fill || !valEl) return;
    const score = Math.max(0, Math.min(100, parseFloat(valEl.getAttribute('data-score')) || 0));
    const r = parseFloat(fill.getAttribute('r')) || 50;
    const c = 2 * Math.PI * r;
    fill.setAttribute('stroke-dasharray', c);
    fill.setAttribute('stroke-dashoffset', c);
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          requestAnimationFrame(() => {
            fill.setAttribute('stroke-dashoffset', c - (c * score) / 100);
          });
          animateCounter(valEl, score, 1600);
          io.unobserve(ring);
        }
      });
    }, { threshold: 0.35 });
    io.observe(ring);
  }

  /* ---------- Radar chart (DNA) ---------- */
  function initRadar() {
    if (!('IntersectionObserver' in window)) return;
    const svg = $('.dna-radar svg');
    
    if (!svg) return;
    const dataAttr = svg.getAttribute('data-values') || '';
    const values = dataAttr.split(',').map((v) => Math.max(0, Math.min(100, parseFloat(v) || 0)));
    if (values.length < 3) return;

    const size = 380;
    const cx = size / 2;
    const cy = size / 2;
    const maxR = size / 2 - 50;
    const labelRadius = maxR + 35;
    const n = values.length;

    // Build grid rings
    const gridGroup = svg.querySelector('.grid');
    if (gridGroup) {
      let g = '';
      for (let s = 1; s <= 4; s++) {
        const rr = (maxR * s) / 4;
        const pts = [];
        for (let i = 0; i < n; i++) {
          const a = (Math.PI * 2 * i) / n - Math.PI / 2;
          pts.push(`${(cx + Math.cos(a) * rr).toFixed(1)},${(cy + Math.sin(a) * rr).toFixed(1)}`);
        }
        g += `<polygon points=\"${pts.join(' ')}\" fill=\"none\" stroke=\"rgba(139,128,255,0.14)\" stroke-width=\"1\"/>`;
      }
      // Axes
      for (let i = 0; i < n; i++) {
        const a = (Math.PI * 2 * i) / n - Math.PI / 2;
        const x = cx + Math.cos(a) * maxR;
        const y = cy + Math.sin(a) * maxR;
        g += `<line x1=\"${cx}\" y1=\"${cy}\" x2=\"${x.toFixed(1)}\" y2=\"${y.toFixed(1)}\" stroke=\"rgba(139,128,255,0.1)\" stroke-width=\"1\"/>`;
      }
      gridGroup.innerHTML = g;
    }

    // Data polygon (start at 0, animate)
    const dataPoly = svg.querySelector('.data-poly');
    const dataDots = svg.querySelector('.data-dots');
    if (!dataPoly) return;

    const targetPts = values.map((v, i) => {
      const a = (Math.PI * 2 * i) / n - Math.PI / 2;
      const rr = (maxR * v) / 100;
      return [cx + Math.cos(a) * rr, cy + Math.sin(a) * rr];
    });
    const zeroPts = values.map(() => [cx, cy]);
    dataPoly.setAttribute('points', zeroPts.map((p) => p.join(',')).join(' '));

    

        // Labels

    const labelsGroup = svg.querySelector(".labels");

    const labels = [
        "Momentum",
        "Discipline",
        "Craft",
        "Influence",
        "Insight",
        "Resolve"
    ];


    if (labelsGroup) {

        let html = "";


        for (let i = 0; i < n; i++) {

            const angle = (Math.PI * 2 * i) / n - Math.PI / 2;

            const x = cx + Math.cos(angle) * labelRadius;
            const y = cy + Math.sin(angle) * labelRadius;


            const anchor =
                (i === 1 || i === 2)
                    ? "start"
                    : (i === 4 || i === 5)
                    ? "end"
                    : "middle";


            html += `
            <text
                class="radar-label"
                x="${x.toFixed(1)}"
                y="${y.toFixed(1)}"
                text-anchor="${anchor}"
                dominant-baseline="middle">
                ${labels[i]}
            </text>
            `;

        }


        labelsGroup.innerHTML = html;

    }




    // Animate
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          const dur = 1400;
          const t0 = performance.now();
          function step(now) {
            const p = Math.min(1, (now - t0) / dur);
            const eased = easeOutExpo(p);
            const pts = targetPts.map(([x, y]) => [cx + (x - cx) * eased, cy + (y - cy) * eased]);
            dataPoly.setAttribute('points', pts.map((p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' '));
            if (dataDots) {
              dataDots.innerHTML = pts
                .map(([x, y]) => `<circle cx=\"${x.toFixed(1)}\" cy=\"${y.toFixed(1)}\" r=\"3\" fill=\"#a78bfa\" stroke=\"#0a0a1a\" stroke-width=\"2\"/>`)
                .join('');
            }
            if (p < 1) requestAnimationFrame(step);
          }
          requestAnimationFrame(step);
          io.unobserve(svg);
        }
      });
    }, { threshold: 0.3 });
    io.observe(svg);
  }

  /* ---------- Language bar composition ---------- */
  const LANG_COLORS = {
    Python: '#3572A5', JavaScript: '#f1e05a', TypeScript: '#3178c6',
    HTML: '#e34c26', CSS: '#563d7c', Java: '#b07219', 'C++': '#f34b7d',
    C: '#555555', 'C#': '#178600', Go: '#00ADD8', Rust: '#dea584',
    Ruby: '#701516', PHP: '#4F5D95', Swift: '#F05138', Kotlin: '#A97BFF',
    Shell: '#89e051', Dockerfile: '#384d54', 'Jupyter Notebook': '#DA5B0B',
    Vue: '#41b883', Dart: '#00B4AB', Scala: '#c22d40', R: '#198CE7',
    Haskell: '#5e5086', Elixir: '#6e4a7e', Perl: '#0298c3',
    Lua: '#000080', 'Objective-C': '#438eff', Assembly: '#6E4C13'
  };

  function initLanguageBar() {
    // Repository page uses .language-item elements with count
    document.querySelectorAll('.language-item').forEach((el) => {
      const name = (el.getAttribute('data-lang') || el.textContent || '').trim().split('\n')[0].trim();
      const color = LANG_COLORS[name] || '#a78bfa';
      el.style.setProperty('--lang-color', color);
    });
    document.querySelectorAll('.project-info .lang').forEach((el) => {
      const name = (el.getAttribute('data-lang') || el.textContent || '').trim();
      const color = LANG_COLORS[name] || '#a78bfa';
      el.style.setProperty('--lang-color', color);
    });

    // Build proportional language bar if present
    const bar = document.querySelector('.language-bar');
    if (!bar) return;
    const items = Array.from(document.querySelectorAll('.language-item'));
    const data = items.map((el) => {
      const name = (el.getAttribute('data-lang') || el.textContent || '').trim().split('\n')[0].trim();
      const count = parseFloat(el.getAttribute('data-count')) || 0;
      return { name, count, color: LANG_COLORS[name] || '#a78bfa' };
    }).filter((d) => d.count > 0);
    const total = data.reduce((s, d) => s + d.count, 0);
    if (!total) return;
    bar.innerHTML = data
      .map((d) => `<span class=\"language-bar-seg\" title=\"${d.name} · ${d.count}\" style=\"width:0%;background:${d.color}\"></span>`)
      .join('');
    const segs = bar.querySelectorAll('.language-bar-seg');
    requestAnimationFrame(() => {
      data.forEach((d, i) => {
        segs[i].style.transition = 'width 1s cubic-bezier(0.2, 0.9, 0.3, 1)';
        segs[i].style.width = ((d.count / total) * 100) + '%';
      });
    });
  }

  /* ---------- Analyze form loading state ---------- */
  function initFormLoading() {
    document.querySelectorAll('form.search-form, form.deep-form').forEach((form) => {
      form.addEventListener('submit', () => {
        const btn = form.querySelector('button[type=\"submit\"]');
        if (btn) {
          btn.classList.add('loading');
          const original = btn.dataset.original || btn.textContent.trim();
          btn.dataset.original = original;
          btn.textContent = 'Analyzing';
        }
      });
    });
  }

  /* ---------- Sample username hint clicks ---------- */
  function initHintClicks() {
    document.querySelectorAll('.search-hint code').forEach((code) => {
      code.addEventListener('click', () => {
        const input = document.querySelector('input[name=\"username\"]');
        if (input) {
          input.value = code.textContent.trim();
          input.focus();
        }
      });
    });
  }

  /* ---------- Repositories: search / sort / filter ---------- */
  function initRepoPage() {
    const list = document.getElementById('repo-list');
    if (!list) return;
    const cards = Array.from(list.querySelectorAll('.repo-card'));
    const search = document.getElementById('repo-search');
    const sortSel = document.getElementById('repo-sort');
    const langSel = document.getElementById('repo-lang');
    const tabs = document.querySelectorAll('.repo-tabs .tab');
    const counter = document.getElementById('repo-count');
    let filter = 'all'; // all|source|fork
    let query = '';
    let sort = 'stars';
    let lang = '';

    function apply() {
      let visible = cards.filter((c) => {
        const isFork = c.dataset.fork === '1';
        if (filter === 'source' && isFork) return false;
        if (filter === 'fork' && !isFork) return false;
        if (lang && (c.dataset.lang || '').toLowerCase() !== lang.toLowerCase()) return false;
        if (query) {
          const hay = ((c.dataset.name || '') + ' ' + (c.dataset.desc || '') + ' ' + (c.dataset.topics || '')).toLowerCase();
          if (!hay.includes(query.toLowerCase())) return false;
        }
        return true;
      });
      visible.sort((a, b) => {
        if (sort === 'stars') return (+b.dataset.stars || 0) - (+a.dataset.stars || 0);
        if (sort === 'forks') return (+b.dataset.forks || 0) - (+a.dataset.forks || 0);
        if (sort === 'updated') return (b.dataset.updated || '').localeCompare(a.dataset.updated || '');
        if (sort === 'name') return (a.dataset.name || '').localeCompare(b.dataset.name || '');
        return 0;
      });
      cards.forEach((c) => (c.style.display = 'none'));
      visible.forEach((c) => (c.style.display = ''));
      visible.forEach((c, i) => (c.style.order = i));
      if (counter) counter.textContent = visible.length + ' / ' + cards.length;
      const empty = document.getElementById('repo-empty');
      if (empty) empty.style.display = visible.length ? 'none' : 'block';
    }

    if (search) search.addEventListener('input', (e) => { query = e.target.value; apply(); });
    if (sortSel) sortSel.addEventListener('change', (e) => { sort = e.target.value; apply(); });
    if (langSel) langSel.addEventListener('change', (e) => { lang = e.target.value; apply(); });
    tabs.forEach((t) => t.addEventListener('click', () => {
      tabs.forEach((x) => x.classList.remove('active'));
      t.classList.add('active');
      filter = t.dataset.filter || 'all';
      apply();
    }));
    apply();
  }

  /* ---------- Toast for placeholder buttons ---------- */
  function toast(msg) {
    let t = document.getElementById('ih-toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'ih-toast';
      t.style.cssText = 'position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(20px);padding:12px 20px;background:rgba(20,22,40,0.95);border:1px solid rgba(160,148,255,0.32);border-radius:12px;color:#ecebff;font-family:JetBrains Mono,monospace;font-size:12px;letter-spacing:0.06em;z-index:200;opacity:0;transition:all 0.35s cubic-bezier(0.2,0.9,0.3,1);backdrop-filter:blur(20px);box-shadow:0 20px 50px -10px rgba(0,0,0,0.6)';
      document.body.appendChild(t);
    }
    t.textContent = msg;
    requestAnimationFrame(() => { t.style.opacity = '1'; t.style.transform = 'translateX(-50%) translateY(0)'; });
    clearTimeout(t._h);
    t._h = setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateX(-50%) translateY(20px)'; }, 2400);
  }

  function initPlaceholders() {
    document.querySelectorAll('[data-placeholder-action]').forEach((el) => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        toast(el.dataset.placeholderAction || 'Coming soon');
      });
    });
  }

  /* ---------- Entrance stagger ---------- */
  function initReveal() {
    if (!('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e, idx) => {
        if (e.isIntersecting) {
          e.target.style.animationDelay = ((idx % 6) * 60) + 'ms';
          e.target.classList.add('fade-up');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('[data-reveal]').forEach((el) => io.observe(el));
  }

  
  /* ---------- Repository Analytics Interactive Cards ---------- */

function initStatCards(){

    const cards = document.querySelectorAll(".stat-card");

    if(!cards.length) return;


    cards.forEach(card => {

        card.addEventListener("click", () => {

            const isOpen = card.classList.contains("active");


            // close every card first
            cards.forEach(c => {
                c.classList.remove("active");
            });


            // open only clicked card
            if(!isOpen){
                card.classList.add("active");
            }

        });

    });

}


/* ---------- Snapshot Intelligence Cards ---------- */

function initSnapshotCards(){

    const cards = document.querySelectorAll(".snapshot-card");

    if(!cards.length) return;


    cards.forEach((card,index)=>{

        card.style.animationDelay = `${index * 100}ms`;

    });

}

    /* ---------- Browser Navigation ---------- */
  function initNavigationButtons() {

    const backBtn = document.querySelector('[data-nav-back]');
    const forwardBtn = document.querySelector('[data-nav-forward]');

    if (backBtn) {
      backBtn.addEventListener('click', () => {
        window.history.back();
      });
    }

    if (forwardBtn) {
      forwardBtn.addEventListener('click', () => {
        window.history.forward();
      });
    }

  }





  /* ---------- Boot ---------- */
  document.addEventListener('DOMContentLoaded', () => {
    initNavigationButtons();
    initCounters();
    initBars();
    initSignalBars();
    initScoreRing();
    initRadar();
    initLanguageBar();
    initFormLoading();
    initHintClicks();
    initRepoPage();
    initPlaceholders();
    initReveal();
    initStatCards();
    initSnapshotCards();
  });
})();
