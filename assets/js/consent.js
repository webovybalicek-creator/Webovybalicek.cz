// Souhlas s cookies (zákon č. 127/2005 Sb. § 89 odst. 3, GDPR). Bez souhlasu se nespustí nic kromě nezbytného.
// Volba se ukládá do cookie wb_consent na 12 měsíců (verze V – při změně kategorií zvýšit, lišta se zobrazí znovu).
// Skripty třetích stran: <script type="text/plain" data-consent="analytics|marketing" [data-src="…"]> se spustí až po souhlasu.
// Google Consent Mode v2: výchozí „denied“ je v <head>, tady se jen aktualizuje.
(() => {
  const NAME = 'wb_consent', V = 1, DAYS = 365, CATS = ['analytics', 'marketing', 'media'];
  const read = () => {
    try {
      const m = document.cookie.match(/(?:^|; )wb_consent=([^;]*)/);
      const c = m && JSON.parse(decodeURIComponent(m[1]));
      return c && c.v === V ? c : null;
    } catch (e) { return null; }
  };
  const run = (c) => {
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', {
        analytics_storage: c.analytics ? 'granted' : 'denied',
        ad_storage: c.marketing ? 'granted' : 'denied',
        ad_user_data: c.marketing ? 'granted' : 'denied',
        ad_personalization: c.marketing ? 'granted' : 'denied',
      });
    }
    document.querySelectorAll('script[type="text/plain"][data-consent]').forEach((old) => {
      if (!c[old.dataset.consent]) return;
      const s = document.createElement('script');
      if (old.dataset.src) { s.src = old.dataset.src; s.async = true; } else s.textContent = old.textContent;
      old.replaceWith(s);
    });
  };
  const bar = document.getElementById('cc-bar');
  const dlg = document.getElementById('cc-settings');
  const save = (choice) => {
    const c = { v: V, ts: new Date().toISOString(), necessary: true };
    CATS.forEach((k) => { c[k] = !!choice[k]; });
    const secure = location.protocol === 'https:' ? '; Secure' : '';
    document.cookie = `${NAME}=${encodeURIComponent(JSON.stringify(c))}; Max-Age=${DAYS * 86400}; Path=/; SameSite=Lax${secure}`;
    if (bar) bar.hidden = true;
    document.documentElement.classList.remove('has-cc');
    run(c);
    document.dispatchEvent(new CustomEvent('wb:consent', { detail: c }));
    return c;
  };
  const all = (on) => Object.fromEntries(CATS.map((k) => [k, on]));
  const openSettings = () => {
    if (!dlg) return;
    const c = read() || {};
    dlg.querySelectorAll('input[data-cat]').forEach((i) => { i.checked = !!c[i.dataset.cat]; });
    document.documentElement.classList.add('is-locked');
    dlg.showModal();
  };
  const closeSettings = () => { if (dlg && dlg.open) dlg.close(); };

  window.wbConsent = {
    get: read,
    allow: (cat) => save({ ...all(false), ...(read() || {}), [cat]: true }),
    open: openSettings,
  };

  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-cc]');
    if (!b) return;
    e.preventDefault();
    const a = b.dataset.cc;
    if (a === 'accept') { save(all(true)); closeSettings(); }
    else if (a === 'reject') { save(all(false)); closeSettings(); }
    else if (a === 'settings') openSettings();
    else if (a === 'save') {
      const ch = {}; dlg.querySelectorAll('input[data-cat]').forEach((i) => { ch[i.dataset.cat] = i.checked; });
      save(ch); closeSettings();
    }
  });

  const c = read();
  if (c) run(c);
  else if (bar) { bar.hidden = false; document.documentElement.classList.add('has-cc'); }
})();
