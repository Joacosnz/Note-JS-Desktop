(() => {
  let busy = false, selected = '', revision = 0, message = 'Conectá Google Calendar para sincronizar tu agenda.', calendars = [], connected = false, syncEnabled = false, email = '';
  async function api(action, body = {}) {
    const response = await fetch('/api/google-calendar/' + action, {method:'POST',headers:{'Content-Type':'application/json','X-NoteJS-Client':'calendar'},body:JSON.stringify(body)});
    const data = await response.json(); if (!response.ok || !data.ok) throw new Error(data.error || 'No se pudo conectar Calendar.'); return data;
  }
  function render() {
    const host = document.querySelector('#reminders-page-view'); if (!host || !host.querySelector('.reminders-full-header')) return;
    let panel = host.querySelector('#google-calendar-panel');
    if (!panel) { panel = document.createElement('section'); panel.id = 'google-calendar-panel'; panel.style.cssText = 'border:1px solid var(--border-hairline);border-radius:14px;padding:16px;margin:0 0 20px;background:var(--bg-surface)'; host.querySelector('.reminders-full-header').after(panel); }
    panel.replaceChildren();
    const title = document.createElement('strong'); title.textContent = 'Google Calendar'; panel.append(title);
    const status = document.createElement('p'); status.setAttribute('role','status'); status.textContent = message; status.style.fontSize='13px'; panel.append(status);
    function button(label, action) { const el=document.createElement('button'); el.type='button'; el.className='btn-secondary'; el.textContent=label; el.disabled=busy; el.style.marginRight='10px'; el.onclick=action; panel.append(el); }
    if (connected) {
      const select = document.createElement('select'); select.setAttribute('aria-label','Calendario de Google'); select.disabled=busy;select.style.cssText='font:inherit;color:var(--text-primary);background:var(--bg-surface);border:1px solid var(--border-hairline);border-radius:8px;padding:6px 10px;margin:0 10px 8px 0;max-width:100%';
      calendars.forEach(c=>{const option=document.createElement('option');option.value=c.id;option.textContent=c.name;select.append(option);});
      select.value=selected;select.onchange=()=>{selected=select.value;syncEnabled=false;message='Calendario seleccionado. Presioná Sincronizar para vincularlo.';render();}; panel.append(select);
      button('Sincronizar ahora', ()=>{syncEnabled=true;try{localStorage.setItem('notejs-calendar:'+email,selected);}catch{}sync();}); button('Desconectar', async()=>{try{await api('disconnect');connected=false;syncEnabled=false;calendars=[];message='Calendar desconectado. Tus recordatorios se conservan.';}catch(e){message=e.message;}render();});
    } else button('Conectar Google Calendar', connect);
  }
  async function connect() {
    if(busy)return;busy=true;let popup;
    try{
      if(!window.pywebview?.api?.open_google_calendar) popup=window.open('about:blank','notejs-calendar');
      const session=await api('start');const url='/google-calendar-connect.html?'+new URLSearchParams({state:session.state});
      if(window.pywebview?.api?.open_google_calendar){const result=await window.pywebview.api.open_google_calendar(session.state);if(!result.ok)throw new Error(result.error);}
      else if(popup)popup.location=url;else throw new Error('Permití abrir el navegador para conectar Calendar.');
      message='Completá el permiso en el navegador y volvé aquí.';render();
      const deadline=Date.now()+300000;let grant;
      while(Date.now()<deadline){await new Promise(r=>setTimeout(r,1500));const result=await api('poll',session);if(result.credential){grant=result.credential;break;}}
      if(!grant)throw new Error('La conexión caducó. Volvé a intentarlo.');
      const data=await api('connect',grant);email=data.email;calendars=data.calendars;connected=true;
      let saved='';try{saved=localStorage.getItem('notejs-calendar:'+email)||'';}catch{} selected=calendars.some(c=>c.id===saved)?saved:(calendars.find(c=>c.primary)||calendars[0])?.id||'';
      message=calendars.length?`Conectado como ${email}. Elegí el calendario y sincronizá.`:'Esta cuenta no tiene calendarios con permiso de escritura.';
    }catch(e){message=e.message;popup?.close();}finally{busy=false;render();}
  }
  async function sync(){
    if(busy||!connected||!syncEnabled||!selected)return;busy=true;message='Sincronizando Calendar…';render();
    const startedRevision=revision;
    try{const data=await api('sync',{calendarId:selected});if(startedRevision===revision)window.applyCalendarReminders?.(data.reminders);else setTimeout(sync,1500);message=`${email} · ${data.imported} recibidos, ${data.exported} enviados, ${data.deleted} eliminados.`+(data.conflicts?` ${data.conflicts} conflictos: se conservaron ambas versiones. Revisalos en Google Calendar antes de volver a sincronizar.`:'');}
    catch(e){message=e.message;try{connected=(await api('status')).connected;}catch{}}
    finally{busy=false;render();}
  }
  // app.js rebuilds the reminders view when changing tabs or completing an item.
  new MutationObserver(()=>{if(!document.querySelector('#google-calendar-panel'))render();}).observe(document.querySelector('#reminders-page-view'),{childList:true});
  setInterval(()=>{if(navigator.onLine)sync();},300000);
  window.addEventListener('online',()=>sync());
  window.addEventListener('notejs-reminder-saved',()=>{revision++;if(connected)setTimeout(sync,1200);});
  api('status').then(async data=>{if(data.connected){const list=await api('calendars');calendars=list.calendars;email=list.email;connected=true;let saved='';try{saved=localStorage.getItem('notejs-calendar:'+email)||'';}catch{} selected=calendars.some(c=>c.id===saved)?saved:(calendars.find(c=>c.primary)||calendars[0])?.id||'';message=`Conectado como ${email}.`;}render();}).catch(()=>render());
})();
