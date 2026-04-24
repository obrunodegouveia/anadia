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
