// Auto-dismiss messages after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
  const messages = document.querySelectorAll('.message');
  messages.forEach(msg => {
    setTimeout(() => {
      msg.style.transition = 'opacity 0.4s, transform 0.4s';
      msg.style.opacity = '0';
      msg.style.transform = 'translateY(-8px)';
      setTimeout(() => msg.remove(), 400);
    }, 4000);
  });

  // Highlight search terms in table
  const searchInput = document.querySelector('.search-input');
  if (searchInput && searchInput.value) {
    const query = searchInput.value.toLowerCase();
    document.querySelectorAll('.app-row td').forEach(cell => {
      const text = cell.innerHTML;
      if (cell.textContent.toLowerCase().includes(query)) {
        cell.innerHTML = text.replace(
          new RegExp(`(${query})`, 'gi'),
          '<mark style="background:rgba(108,143,255,0.25);color:inherit;border-radius:3px;padding:0 2px;">$1</mark>'
        );
      }
    });
  }

  // Set today's date as default for date_applied field on add form
  const dateField = document.querySelector('#id_date_applied');
  if (dateField && !dateField.value) {
    dateField.value = new Date().toISOString().split('T')[0];
  }
});
