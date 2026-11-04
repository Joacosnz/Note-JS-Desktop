(() => {
  let returnFocus;
  const menu = () => document.getElementById('desktop-app-menu');
  const trigger = () => document.getElementById('desktop-menu-trigger');
  function close() {
    if (!menu() || menu().hidden) return;
    menu().hidden = true; trigger().setAttribute('aria-expanded','false');
  }
  window.toggleDesktopMenu = () => {
    const opening = menu().hidden;
    close();
    if (opening) {
      returnFocus = document.activeElement;
      menu().hidden = false; trigger().setAttribute('aria-expanded','true');
      menu().querySelector('[role=menuitem]')?.focus();
    }
  };
  window.openCloudSettings = () => { close(); openSettingsModal(); switchSettingsSection('account'); };
  document.addEventListener('click', event => {
    const projectLink = event.target.closest('a[data-project-link]');
    if (projectLink && window.pywebview?.api?.open_project_link) {
      event.preventDefault();
      window.pywebview.api.open_project_link(projectLink.href).then(result => {
        document.getElementById('project-link-status').textContent = result?.ok ? '' : 'No se pudo abrir el navegador. Podés copiar la dirección del enlace.';
      }).catch(() => {
        document.getElementById('project-link-status').textContent = 'No se pudo abrir el navegador. Podés copiar la dirección del enlace.';
      });
    }
    document.querySelectorAll('.page-tools[open]').forEach(details => { if (!details.contains(event.target) || event.target.closest('button')) details.open = false; });
    if (!event.target.closest('#desktop-app-menu, #desktop-menu-trigger')) close();
    const item = event.target.closest('#desktop-app-menu [data-menu-action]');
    if (!item) return;
    close();
    const actions = {
      note:() => createNewNote(), pdf:() => document.getElementById('open-pdf-file').click(),
      search:() => openQuickFindModal(), folder:() => promptNewFolder(),
      home:() => navigateToHome(), reminders:() => navigateToReminders(),
      settings:() => openSettingsModal(), account:() => window.openCloudSettings(),
      sync:() => window.NoteJSCloud?.syncNow(), shortcuts:() => openShortcutsModal()
    };
    actions[item.dataset.menuAction]?.();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') document.querySelectorAll('.page-tools[open]').forEach(details => { details.open = false; details.querySelector('summary').focus(); });
    if (!menu() || menu().hidden) return;
    if (event.key === 'Escape') { event.preventDefault(); close(); returnFocus?.focus(); return; }
    if (event.key === 'Tab') { close(); return; }
    const items = [...menu().querySelectorAll('[role=menuitem]')].filter(item => !item.disabled);
    let index = items.indexOf(document.activeElement);
    if (['ArrowDown','ArrowUp','Home','End'].includes(event.key)) {
      event.preventDefault();
      index = event.key === 'Home' ? 0 : event.key === 'End' ? items.length-1 : (index + (event.key === 'ArrowDown' ? 1 : -1) + items.length) % items.length;
      items[index]?.focus();
    }
  });
  window.addEventListener('notejs:cloud-status', event => {
    const {message,connected,name,pending} = event.detail;
    document.getElementById('desktop-cloud-detail').textContent = message;
    const label = !connected ? 'En esta PC' : message.startsWith('Conectado.') ? 'Al día' : /Sin conexión/i.test(message) ? 'Sin conexión' : /Sincronizando/i.test(message) ? 'Sincronizando…' : pending ? `${pending} pendientes` : 'Conectando…';
    document.getElementById('sidebar-cloud-label').textContent = label;
    document.getElementById('sidebar-account-name').textContent = name || 'Tu biblioteca';
    const status = document.getElementById('sidebar-account');
    status.title = message; status.dataset.cloud = connected ? (label === 'Al día' ? 'synced' : 'pending') : 'local';
    const navName = document.querySelector('.notion-nav-user-name');
    if (navName) navName.textContent = name || 'Mi cuenta';
  });
})();
