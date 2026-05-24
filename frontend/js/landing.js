/** Atlas landing page — Get Started flow (no login) */

export function initLanding(onStart) {
  const landing = document.getElementById('landing-page');
  const nav = document.querySelector('.landing-nav');
  const getStartedBtn = document.getElementById('btn-get-started');
  const exploreBtn = document.getElementById('btn-explore-features');

  if (!landing || !getStartedBtn) return;

  const startSession = () => {
    sessionStorage.setItem('atlas_started', '1');
    enterApp(landing, onStart);
  };

  getStartedBtn.addEventListener('click', startSession);
  document.getElementById('btn-get-started-nav')?.addEventListener('click', startSession);

  if (exploreBtn) {
    exploreBtn.addEventListener('click', () => {
      document.getElementById('landing-pillars')?.scrollIntoView({ behavior: 'smooth' });
    });
  }

  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) nav?.classList.add('scrolled');
    else nav?.classList.remove('scrolled');
  }, { passive: true });

  if (sessionStorage.getItem('atlas_started') === '1') {
    landing.classList.add('is-hidden');
    onStart?.();
  }
}

export function enterApp(landingEl, onStart) {
  landingEl.classList.add('is-hidden');
  setTimeout(() => {
    landingEl.style.display = 'none';
    onStart?.();
  }, 650);
}

export function showLanding() {
  const landing = document.getElementById('landing-page');
  const dashboard = document.getElementById('app-dashboard');
  sessionStorage.removeItem('atlas_started');
  dashboard?.classList.remove('is-active');
  document.body.classList.remove('app-mode');
  if (landing) {
    landing.style.display = 'flex';
    landing.classList.remove('is-hidden');
  }
}
