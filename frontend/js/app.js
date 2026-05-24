import { initLanding } from './landing.js';
import { initChat } from './chat.js';

function activateDashboard() {
  const dashboard = document.getElementById('app-dashboard');
  document.body.classList.add('app-mode');
  dashboard?.classList.add('is-active');
  if (window.feather) feather.replace();
  initChat();
}

document.addEventListener('DOMContentLoaded', () => {
  if (window.feather) feather.replace();
  initLanding(activateDashboard);
  if (sessionStorage.getItem('atlas_started') === '1') {
    activateDashboard();
  }
});
