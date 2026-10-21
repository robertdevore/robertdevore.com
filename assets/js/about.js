/* Progressive enhancement: the complete sourced index is present without JavaScript. */
(() => {
  const form = document.querySelector('.about-filter');
  const records = Array.from(document.querySelectorAll('#disclosure-records > li'));
  if (!form || !records.length) return;
  const search = document.getElementById('disclosure-search');
  const severity = document.getElementById('disclosure-severity');
  const status = document.getElementById('disclosure-status');
  const empty = document.getElementById('disclosure-empty');
  const text = records.map(record => record.textContent.toLowerCase());
  function filter() {
    const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    records.forEach((record, index) => {
      record.hidden = !terms.every(term => text[index].includes(term)) ||
        Boolean(severity.value && record.dataset.severity !== severity.value);
      if (!record.hidden) count++;
    });
    status.textContent = `${count} of ${records.length} disclosures`;
    empty.hidden = count !== 0;
  }
  form.hidden = false;
  form.addEventListener('submit', event => event.preventDefault());
  search.addEventListener('input', filter);
  severity.addEventListener('change', filter);
  form.addEventListener('reset', () => {
    search.value = '';
    severity.value = '';
    filter();
    search.focus();
  });
  filter();
})();
