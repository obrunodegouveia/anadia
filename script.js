// =================== i18n ===================
const I18N_LANGS = ['en', 'pt', 'de', 'fr', 'es'];
const I18N_DEFAULT = 'en';

const I18N_PATH = { en: '/', pt: '/pt/', de: '/de/', fr: '/fr/', es: '/es/' };

function langFromPath() {
  const p = location.pathname;
  for (const lang of I18N_LANGS) {
    if (lang === 'en') continue;
    if (p === `/${lang}/` || p === `/${lang}` || p.startsWith(`/${lang}/`)) return lang;
  }
  return 'en';
}

function detectLang() {
  // 1. URL path takes priority (we have static /pt/ pages)
  const path = langFromPath();
  if (path !== 'en' || location.pathname === '/' || location.pathname === '/index.html') {
    // path tells us the right answer if we are on /pt/, or we are on root and English is the default
    return path;
  }
  // 2. ?lang= query param (legacy)
  const url = new URLSearchParams(location.search).get('lang');
  if (url && I18N_LANGS.includes(url)) return url;
  // 3. localStorage
  const stored = localStorage.getItem('lang');
  if (stored && I18N_LANGS.includes(stored)) return stored;
  // 4. browser
  const browser = (navigator.language || 'en').slice(0, 2).toLowerCase();
  if (I18N_LANGS.includes(browser)) return browser;
  return I18N_DEFAULT;
}

// On root URL, redirect to the user's preferred language if it differs from default
function maybeRedirectFromRoot() {
  if (location.pathname !== '/' && location.pathname !== '/index.html') return;
  if (new URLSearchParams(location.search).get('lang')) return; // user explicitly asked
  const stored = localStorage.getItem('lang');
  if (stored && stored !== 'en' && I18N_PATH[stored]) {
    location.replace(I18N_PATH[stored]);
  }
}
maybeRedirectFromRoot();

let translations = null;

async function loadTranslations() {
  if (translations) return translations;
  try {
    const res = await fetch('/i18n.json', { cache: 'force-cache' });
    translations = await res.json();
  } catch (e) {
    console.warn('i18n load failed', e);
    translations = { en: {}, pt: {} };
  }
  return translations;
}

function applyLang(lang) {
  const dict = (translations && translations[lang]) || {};
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const k = el.getAttribute('data-i18n');
    if (dict[k] != null) el.textContent = dict[k];
  });
  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    const k = el.getAttribute('data-i18n-html');
    if (dict[k] != null) el.innerHTML = dict[k];
  });
  // Attribute translations: data-i18n-attr-XYZ="key" → set attribute XYZ
  document.querySelectorAll('*').forEach(el => {
    for (const attr of el.attributes) {
      if (attr.name.startsWith('data-i18n-attr-')) {
        const target = attr.name.slice('data-i18n-attr-'.length);
        const k = attr.value;
        if (dict[k] != null) el.setAttribute(target, dict[k]);
      }
    }
  });
  // Update active state on switcher
  document.querySelectorAll('.lang-switch__btn').forEach(b => {
    b.classList.toggle('is-active', b.dataset.lang === lang);
  });
}

async function initI18n() {
  const docLang = document.documentElement.lang;
  const targetLang = detectLang();
  // If the page is already statically rendered in the requested language,
  // skip fetching i18n.json — saves ~28 KB on every PT page load.
  if (docLang !== targetLang) {
    await loadTranslations();
    applyLang(targetLang);
  } else {
    document.querySelectorAll('.lang-switch__btn').forEach(b => {
      b.classList.toggle('is-active', b.dataset.lang === targetLang);
    });
  }
  document.querySelectorAll('.lang-switch__btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const newLang = btn.dataset.lang;
      localStorage.setItem('lang', newLang);
      const target = I18N_PATH[newLang];
      if (target && target !== location.pathname) {
        location.href = target;
      } else {
        loadTranslations().then(() => applyLang(newLang));
      }
    });
  });
}
initI18n();

// Mobile nav toggle
const nav = document.getElementById('nav');
const toggle = document.getElementById('navToggle');
if (toggle && nav) {
  toggle.addEventListener('click', () => nav.classList.toggle('is-open'));
  nav.querySelectorAll('.nav__links a, .nav__cta').forEach(a => {
    a.addEventListener('click', () => nav.classList.remove('is-open'));
  });
}

// Footer year
const yr = document.getElementById('year');
if (yr) yr.textContent = new Date().getFullYear();

// Gallery filters
const filters = document.querySelectorAll('.gallery__filters .chip');
const items   = Array.from(document.querySelectorAll('#gallery .gallery__item'));
filters.forEach(btn => {
  btn.addEventListener('click', () => {
    filters.forEach(f => f.classList.remove('is-active'));
    btn.classList.add('is-active');
    const cat = btn.dataset.filter;
    items.forEach(it => {
      it.classList.toggle('is-hidden', cat !== 'all' && it.dataset.cat !== cat);
    });
  });
});

// Lightbox
const lb     = document.getElementById('lightbox');
const lbImg  = document.getElementById('lbImg');
const lbCap  = document.getElementById('lbCap');
const lbPrev = document.getElementById('lbPrev');
const lbNext = document.getElementById('lbNext');
const lbClose= document.getElementById('lbClose');

let visibleItems = [];
let currentIdx = 0;

function visible() {
  return items.filter(it => !it.classList.contains('is-hidden'));
}
const lbCounter = document.getElementById('lbCounter');
function openAt(idx) {
  visibleItems = visible();
  currentIdx = (idx + visibleItems.length) % visibleItems.length;
  const fig = visibleItems[currentIdx];
  const img = fig.querySelector('img');
  const cap = fig.querySelector('figcaption');
  lbImg.src = img.src;
  lbImg.alt = img.alt || '';
  lbCap.textContent = cap ? cap.textContent : '';
  if (lbCounter) lbCounter.textContent = `${currentIdx + 1} / ${visibleItems.length}`;
  lb.classList.add('is-open');
  document.body.style.overflow = 'hidden';
}
function close() {
  lb.classList.remove('is-open');
  document.body.style.overflow = '';
}
items.forEach((it, idx) => {
  it.style.cursor = 'zoom-in';
  it.addEventListener('click', () => openAt(visible().indexOf(it)));
});
lbPrev?.addEventListener('click', e => { e.stopPropagation(); openAt(currentIdx - 1); });
lbNext?.addEventListener('click', e => { e.stopPropagation(); openAt(currentIdx + 1); });
lbClose?.addEventListener('click', close);
lb?.addEventListener('click', e => { if (e.target === lb) close(); });
document.addEventListener('keydown', e => {
  if (!lb.classList.contains('is-open')) return;
  if (e.key === 'Escape')     close();
  if (e.key === 'ArrowLeft')  openAt(currentIdx - 1);
  if (e.key === 'ArrowRight') openAt(currentIdx + 1);
});

// =================== Touch swipe in lightbox ===================
let touchStartX = 0, touchStartY = 0;
lb?.addEventListener('touchstart', e => {
  touchStartX = e.changedTouches[0].clientX;
  touchStartY = e.changedTouches[0].clientY;
}, { passive: true });
lb?.addEventListener('touchend', e => {
  const dx = e.changedTouches[0].clientX - touchStartX;
  const dy = e.changedTouches[0].clientY - touchStartY;
  if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
    if (dx > 0) openAt(currentIdx - 1);
    else        openAt(currentIdx + 1);
  }
}, { passive: true });

// =================== Scroll progress + back-to-top + sticky CTA ===================
const progressBar = document.getElementById('scrollProgress');
const backBtn     = document.getElementById('backToTop');
const mobileCta   = document.getElementById('mobileCta');

function onScroll() {
  const doc = document.documentElement;
  const max = doc.scrollHeight - doc.clientHeight;
  const pct = max > 0 ? (doc.scrollTop / max) * 100 : 0;
  if (progressBar) progressBar.style.width = pct + '%';

  const past = doc.scrollTop > 600;
  backBtn?.classList.toggle('is-visible', past);

  // Show mobile CTA after first viewport, hide near the contact form (where the form already is)
  const contact = document.getElementById('contact');
  const contactTop = contact ? contact.getBoundingClientRect().top + window.scrollY : Infinity;
  const nearContact = doc.scrollTop + doc.clientHeight > contactTop + 100;
  mobileCta?.classList.toggle('is-visible', past && !nearContact);
}
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

backBtn?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// =================== Active nav section ===================
const navAnchors = document.querySelectorAll('.nav__links a[href^="#"]');
const sectionMap = new Map();
navAnchors.forEach(a => {
  const id = a.getAttribute('href').slice(1);
  const sec = document.getElementById(id);
  if (sec) sectionMap.set(sec, a);
});
if ('IntersectionObserver' in window && sectionMap.size) {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(en => {
      const link = sectionMap.get(en.target);
      if (!link) return;
      if (en.isIntersecting) {
        navAnchors.forEach(l => l.classList.remove('is-active'));
        link.classList.add('is-active');
      }
    });
  }, { rootMargin: '-40% 0px -55% 0px', threshold: 0 });
  sectionMap.forEach((_, sec) => obs.observe(sec));
}

// =================== Dynamic gallery filter counts ===================
function updateChipCounts() {
  document.querySelectorAll('.gallery__filters .chip').forEach(chip => {
    const cat = chip.dataset.filter;
    const count = cat === 'all'
      ? items.length
      : items.filter(it => it.dataset.cat === cat).length;
    let badge = chip.querySelector('span');
    if (badge) badge.textContent = count;
    else {
      // For chips that don't have a count badge yet
      badge = document.createElement('span');
      badge.textContent = count;
      chip.appendChild(document.createTextNode(' '));
      chip.appendChild(badge);
    }
  });
}
updateChipCounts();

// =================== Show form success after Formsubmit redirect ===================
if (new URLSearchParams(location.search).get('sent') === '1') {
  const success = document.getElementById('contactSuccess');
  if (success) {
    success.hidden = false;
    success.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

// =================== Currency switcher (live FX) ===================
const CCY_FALLBACK = { EUR: 1.0, USD: 1.07, GBP: 0.85, BRL: 5.50 };
const CCY_LOCALE   = { EUR: 'de-DE', USD: 'en-US', GBP: 'en-GB', BRL: 'pt-BR' };
let ccyRates = { ...CCY_FALLBACK };
let ccyCurrent = localStorage.getItem('ccy') || 'EUR';

function fmtCcy(eurAmount, ccy) {
  const rate = ccyRates[ccy] || 1;
  const value = eurAmount * rate;
  try {
    return new Intl.NumberFormat(CCY_LOCALE[ccy] || 'en-US', {
      style: 'currency', currency: ccy, maximumFractionDigits: 0,
    }).format(value);
  } catch {
    return `${ccy} ${Math.round(value).toLocaleString()}`;
  }
}

function applyCurrency(ccy) {
  ccyCurrent = ccy;
  // Update main price display
  document.querySelectorAll('[data-eur]').forEach(el => {
    const eur = parseFloat(el.dataset.eur);
    if (isNaN(eur)) return;
    if (ccy === 'EUR') {
      el.textContent = fmtCcy(eur, 'EUR');
    } else {
      el.textContent = fmtCcy(eur, 'EUR');
    }
  });
  // Show "≈ $X" approx line if not EUR
  const fx = document.getElementById('heroFx');
  if (fx) {
    if (ccy === 'EUR') {
      fx.hidden = true;
      fx.textContent = '';
    } else {
      fx.hidden = false;
      fx.textContent = `≈ ${fmtCcy(parseFloat(document.querySelector('[data-eur]').dataset.eur), ccy)}`;
    }
  }
  // Update active state
  document.querySelectorAll('.ccy-switch__btn').forEach(b => {
    b.classList.toggle('is-active', b.dataset.ccy === ccy);
  });
}

async function initCurrency() {
  // Wire buttons immediately so they work before fetch completes
  document.querySelectorAll('.ccy-switch__btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const ccy = btn.dataset.ccy;
      localStorage.setItem('ccy', ccy);
      applyCurrency(ccy);
    });
  });
  applyCurrency(ccyCurrent);
  // Fetch live rates from Frankfurter (free, ECB rates, no key)
  try {
    const res = await fetch('https://api.frankfurter.app/latest?from=EUR&to=USD,GBP,BRL', { cache: 'force-cache' });
    const data = await res.json();
    if (data && data.rates) {
      ccyRates = { EUR: 1.0, ...data.rates };
      applyCurrency(ccyCurrent);
    }
  } catch (e) {
    // Silent — fallback rates are already in place
  }
}
initCurrency();
