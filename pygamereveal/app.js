const deck = new Reveal({
  hash: true,
  controls: true,
  progress: true,
  center: false,
  transition: 'slide',
  width: 1280,
  height: 720,
  margin: 0,
  minScale: 0.2,
  maxScale: 1.5
});
deck.initialize();

const menu = document.getElementById('module-menu');
const menuButton = document.getElementById('menu-button');
const sectionLabel = document.getElementById('section-label');
const status = document.getElementById('copy-status');
let statusTimer;
let lastCodeBox = null;

function toggleMenu(force) {
  const opened = force ?? !menu.classList.contains('open');
  menu.classList.toggle('open', opened);
  menuButton.setAttribute('aria-expanded', String(opened));
}

function jumpTo(id) {
  const target = document.getElementById(id);
  if (!target) return false;
  const slide = target.closest('.slides section.content-slide, .slides section.module-title, .slides section.cover');
  if (!slide) return false;
  const indices = deck.getIndices(slide);
  deck.slide(indices.h, indices.v);
  toggleMenu(false);
  return true;
}

function showStatus(message) {
  status.textContent = message;
  status.classList.add('visible');
  clearTimeout(statusTimer);
  statusTimer = setTimeout(() => status.classList.remove('visible'), 1900);
}

async function copyCode(box) {
  const code = box?.querySelector('pre code, pre');
  if (!code) return;
  const value = code.textContent.replace(/\n+$/, '');
  try {
    if (!navigator.clipboard?.writeText) throw new Error('clipboard unavailable');
    await navigator.clipboard.writeText(value);
  } catch {
    const area = document.createElement('textarea');
    area.value = value;
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.appendChild(area);
    area.select();
    const copied = document.execCommand('copy');
    area.remove();
    if (!copied) {
      showStatus('Não foi possível copiar');
      return;
    }
  }
  showStatus('Código copiado');
}

menuButton.addEventListener('click', () => toggleMenu());
menu.addEventListener('click', event => {
  const link = event.target.closest('a[data-jump]');
  if (!link) return;
  event.preventDefault();
  jumpTo(link.dataset.jump);
});
document.addEventListener('click', event => {
  const button = event.target.closest('.copy-code');
  if (button) {
    event.preventDefault();
    event.stopPropagation();
    lastCodeBox = button.closest('.code-box');
    copyCode(lastCodeBox);
    return;
  }
  const link = event.target.closest('a[href^="#"]');
  if (link && !link.hasAttribute('data-jump')) {
    const id = decodeURIComponent(link.getAttribute('href').slice(1));
    if (id && jumpTo(id)) event.preventDefault();
  }
});
document.addEventListener('mouseover', event => {
  const box = event.target.closest('.code-box');
  if (box) lastCodeBox = box;
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu.classList.contains('open')) {
    toggleMenu(false);
    event.stopPropagation();
  }
  if (event.key.toLowerCase() === 'm' && !event.altKey && !event.ctrlKey && !event.metaKey && !/INPUT|TEXTAREA/.test(event.target.tagName)) {
    event.preventDefault();
    toggleMenu();
  }
  if (event.altKey && event.code === 'KeyC') {
    event.preventDefault();
    const current = deck.getCurrentSlide();
    const box = current?.contains(lastCodeBox) ? lastCodeBox : current?.querySelector('.code-box');
    if (box) copyCode(box);
    else showStatus('Este slide não contém código');
  }
});
deck.on('slidechanged', event => {
  sectionLabel.textContent = event.currentSlide?.dataset.section || '';
  lastCodeBox = null;
  toggleMenu(false);
});
sectionLabel.textContent = deck.getCurrentSlide()?.dataset.section || '';
