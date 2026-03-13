// Career Track Hub — Main JS

document.addEventListener('DOMContentLoaded', () => {

  // ─── Auto-dismiss messages ───
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-8px)';
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });

  // ─── Active nav link ───
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath.startsWith(href) && href !== '/') {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });

  // ─── Confirm delete ───
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', e => {
      if (!confirm(btn.dataset.confirm || 'Are you sure?')) {
        e.preventDefault();
      }
    });
  });

  // ─── Table row clickable ───
  document.querySelectorAll('tr[data-href]').forEach(row => {
    row.style.cursor = 'pointer';
    row.addEventListener('click', e => {
      if (!e.target.closest('a, button, .btn')) {
        window.location.href = row.dataset.href;
      }
    });
  });

  // ─── Mobile Drawer ───
  const hamburgerBtn  = document.getElementById('hamburgerBtn');
  const drawerCloseBtn = document.getElementById('drawerCloseBtn');
  const mobileDrawer  = document.getElementById('mobileDrawer');
  const mobileOverlay = document.getElementById('mobileOverlay');

  function openDrawer() {
    mobileDrawer.classList.add('open');
    mobileOverlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // prevent background scroll
  }

  function closeDrawer() {
    mobileDrawer.classList.remove('open');
    mobileOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (hamburgerBtn)   hamburgerBtn.addEventListener('click', openDrawer);
  if (drawerCloseBtn) drawerCloseBtn.addEventListener('click', closeDrawer);
  if (mobileOverlay)  mobileOverlay.addEventListener('click', closeDrawer);

  // Close drawer if user presses Escape key
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeDrawer();
  });

});
