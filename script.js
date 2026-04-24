// =================== i18n ===================
const I18N_LANGS = ['en', 'pt'];
const I18N_DEFAULT = 'en';

const I18N_PATH = { pt: '/pt/', en: '/' };

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
  await loadTranslations();
  const lang = detectLang();
  applyLang(lang);
  document.querySelectorAll('.lang-switch__btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const newLang = btn.dataset.lang;
      localStorage.setItem('lang', newLang);
      // If the static page for this lang exists, navigate to it
      const target = I18N_PATH[newLang];
      if (target && target !== location.pathname) {
        location.href = target;
      } else {
        applyLang(newLang);
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
function openAt(idx) {
  visibleItems = visible();
  currentIdx = (idx + visibleItems.length) % visibleItems.length;
  const fig = visibleItems[currentIdx];
  const img = fig.querySelector('img');
  const cap = fig.querySelector('figcaption');
  lbImg.src = img.src;
  lbImg.alt = img.alt || '';
  lbCap.textContent = cap ? cap.textContent : '';
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
