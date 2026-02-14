document.addEventListener('DOMContentLoaded', function () {
  // delegate clicks on the main project card link to open modal
  // (only targets the anchor with class `card-link` so action buttons like Demo/Código keep working)
  document.querySelectorAll('.card-link').forEach(function (el) {
    el.addEventListener('click', function (e) {
      // If user held ctrl/meta or middle click, allow opening in new tab
      if (e.ctrlKey || e.metaKey || e.button === 1) return;
      e.preventDefault();
      const href = el.getAttribute('href') || '';
      // href expected to be like /project/owner/repo
      const parts = href.split('/').filter(Boolean);
      if (parts.length >= 3 && parts[0] === 'project') {
        const owner = parts[1];
        const repo = parts[2];
        openProjectModal(owner, repo);
      }
    });
  });

  function openProjectModal(owner, repo) {
    const modal = document.getElementById('modal-root');
    if (!modal) return;
    modal.innerHTML = `<div class="modal-backdrop"></div>
      <div class="modal" role="dialog" aria-modal="true">
        <button class="modal-close" aria-label="Cerrar">×</button>
        <div class="modal-inner">
          <div class="modal-body-loading">Cargando…</div>
        </div>
      </div>`;

    modal.classList.add('open');
    // focus trap basic
    modal.querySelector('.modal-close').focus();

    // close handlers
    modal.querySelector('.modal-close').addEventListener('click', closeModal);
    modal.querySelector('.modal-backdrop').addEventListener('click', closeModal);
    document.addEventListener('keydown', escClose);

    // fetch project data
    fetch(`/api/project/${owner}/${repo}`)
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (data.error) {
          showError('Proyecto no encontrado');
          return;
        }
        renderModalContent(data.project, data.readme_html);
      })
      .catch(function (err) {
        showError('Error al cargar el proyecto');
        console.error(err);
      });

    function escClose(e) { if (e.key === 'Escape') closeModal(); }
    function closeModal() {
      document.removeEventListener('keydown', escClose);
      modal.classList.remove('open');
      // allow animation before clearing
      setTimeout(() => { modal.innerHTML = ''; }, 300);
    }

    function showError(msg) {
      const inner = modal.querySelector('.modal-inner');
      inner.innerHTML = `<div class="modal-error">${escapeHtml(msg)}</div>`;
    }

    function renderModalContent(project, readme_html) {
      const img = project.preview ? `<img src="${escapeHtml(project.preview)}" alt="preview"/>` : `<img src="/static/placeholder.svg" alt="placeholder"/>`;
      const title = escapeHtml(project.title || project.name || 'Proyecto');
      const desc = escapeHtml(project.description || '');
      const meta = `<div class="modal-meta">${escapeHtml(project.language || '')} • ★ ${project.stargazers_count || 0}</div>`;
      const demoBtn = project.homepage ? `<a class="btn" href="${escapeHtml(project.homepage)}" target="_blank">Demo</a>` : '';

      const inner = modal.querySelector('.modal-inner');
      inner.innerHTML = `
        <div class="modal-grid">
          <div class="modal-column modal-image">${img}</div>
          <div class="modal-column modal-info">
            <h2>${title}</h2>
            <p class="muted">${desc}</p>
            ${meta}
            <div style="margin-top:0.8rem">${demoBtn} <a class="btn" href="${escapeHtml(project.html_url)}" target="_blank" style="margin-left:0.6rem">Código</a></div>
          </div>
        </div>
        <div class="modal-readme">${readme_html || '<p>No hay README disponible.</p>'}</div>
      `;

      // focus close button again for accessibility
      modal.querySelector('.modal-close').focus();
      // ensure links with target="_blank" open reliably (some browsers/extensions may block default behavior inside injected HTML)
      const modalInner = modal.querySelector('.modal-inner');
      modalInner.addEventListener('click', function (ev) {
        const a = ev.target.closest && ev.target.closest('a');
        if (!a) return;
        const href = a.getAttribute('href') || a.href;
        const target = a.getAttribute('target');
        // allow mailto and anchors to behave normally
        if (!href || href.startsWith('#') || href.startsWith('mailto:')) return;
        if (target === '_blank') {
          ev.preventDefault();
          try { window.open(href, '_blank'); } catch (e) { window.location.href = href; }
        }
      });
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str).replace(/[&<>"]+/g, function (s) {
        return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[s];
      });
    }
  }
});
