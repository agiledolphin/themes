// Injected into the Obsidian window by run.mjs; exposes window.__V.
// Opens the test note in a NEW tab (the user's tabs are left alone), switches
// theme / mode / variant and view mode, scrolls to sections, and reads computed styles.
window.__V = (() => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  let cfg = null, leaf = null;

  async function init(config) {
    cfg = config;
    const file = app.vault.getAbstractFileByPath(cfg.note);
    if (!file) throw new Error(`Test note not found in vault: ${cfg.note}`);
    leaf = app.workspace.getLeaf('tab');
    await leaf.openFile(file, { state: { mode: 'preview' } });
    app.workspace.setActiveLeaf(leaf, { focus: true });
    await sleep(800);
    // heading text -> line number, so sections survive edits to the note
    const lines = {};
    for (const h of app.metadataCache.getFileCache(file)?.headings || []) lines[h.heading] ??= h.position.start.line;
    return lines;
  }

  async function variant(theme, mode, cls) {
    if (app.customCss.theme !== theme) { app.customCss.setTheme(theme); await sleep(900); }
    const want = mode === 'dark' ? 'obsidian' : 'moonstone';
    if (app.vault.getConfig('theme') !== want) { app.changeTheme(want); await sleep(600); }
    cfg.variantClasses.forEach(c => document.body.classList.remove(c));
    document.body.classList.add(cls);
    await sleep(500);
  }

  async function viewMode(m) {
    const st = leaf.view.getState();
    await leaf.setViewState({ type: 'markdown', state: { ...st, mode: m === 'reading' ? 'preview' : 'source', source: false } });
    await sleep(700);
    if (m === 'live') {           // park the cursor at the end so no checked line shows raw markdown
      const ed = leaf.view.editor; ed.setCursor(ed.lastLine(), 0); await sleep(200);
    }
  }

  async function scrollTo(line, heading) {
    const v = leaf.view;
    if (v.getMode() === 'preview') {
      // Reading view renders lazily and embeds shift line offsets: approach by line, then snap to the heading.
      for (let i = 0; i < 2; i++) { v.previewMode.applyScroll(line); await sleep(450); }
      const h = [...v.containerEl.querySelectorAll('.markdown-preview-sizer > div > :is(h1, h2, h3, h4)')]
        .find(e => e.textContent.trim() === heading);
      if (h) { h.scrollIntoView({ block: 'start' }); await sleep(450); }
      return;
    }
    const cm = v.editor.cm;      // scroll without moving the cursor
    for (let i = 0; i < 3; i++) {
      cm.scrollDOM.scrollTop = cm.lineBlockAt(cm.state.doc.line(line + 1).from).top - 10;
      await sleep(350);
    }
  }

  // Sections whose content renders asynchronously: wait (up to 5 s) until it is on screen.
  const SETTLE = { mermaid: '.mermaid svg' };
  async function settle(section) {
    const sel = SETTLE[section];
    if (!sel) return;
    const root = leaf.view.containerEl, view = root.querySelector('.view-content').getBoundingClientRect();
    for (let t = 0; t < 5000; t += 100) {
      if ([...root.querySelectorAll(sel)].some(e => { const r = e.getBoundingClientRect(); return r.height > 0 && r.bottom > view.top && r.top < view.bottom; })) {
        await sleep(300); return;
      }
      await sleep(100);
    }
  }

  function rect() {
    const r = leaf.view.containerEl.querySelector('.view-content').getBoundingClientRect();
    return { x: r.x, y: r.y, width: r.width, height: r.height };
  }

  const pick = (el, props, pseudo) => {
    if (!el) return null;
    const s = getComputedStyle(el, pseudo), o = {};
    props.forEach(p => (o[p] = s.getPropertyValue(p)));
    return o;
  };

  // Which measurements belong to which section: each is taken only while its section is
  // scrolled into view, from the first VISIBLE match, so results don't depend on what the
  // (lazily rendered) view happened to have in the DOM.
  const SECTION_KEYS = {
    top: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
    text: ['body', 'mark', 'link', 'unresolved'],
    'quote-code': ['quoteRule', 'quoteText', 'inlineCode', 'codeFrame', 'codeText'],
    tables: ['table', 'th', 'td', 'cellPad'],
    callouts: ['calloutNote', 'calloutNoteBg'],
    hr: ['hr'],
    tags: ['tag', 'tdCode'],
  };
  function measure(section) {
    const root = leaf.view.containerEl, live = leaf.view.getMode() !== 'preview';
    const view = root.querySelector('.view-content').getBoundingClientRect();
    const visible = e => { const r = e.getBoundingClientRect(); return r.height > 0 && r.bottom > view.top && r.top < view.bottom; };
    // first visible match that is part of the note itself, not of an embedded note
    const q = s => [...root.querySelectorAll(s)].find(e => !e.closest('.markdown-embed, .internal-embed') && visible(e)) || null;
    const T = ['color', 'font-size', 'font-family', 'line-height', 'background-color'];
    const B = ['border-top-width', 'border-top-color', 'border-left-width', 'border-left-color', 'border-top-left-radius'];
    const P = ['padding-top', 'padding-left', 'padding-right'];
    const table = q(live ? '.cm-table-widget table' : '.markdown-preview-view table');
    const quoteLine = live ? q('.HyperMD-quote') : null;
    const heading = n => pick(q(live ? `.cm-header-${n}` : `.markdown-preview-view h${n}`), T);
    const all = {
      body: pick(q(live ? '.cm-line:not(.HyperMD-header):not(.HyperMD-codeblock)' : '.markdown-preview-view p'), T),
      h1: heading(1), h2: heading(2), h3: heading(3), h4: heading(4), h5: heading(5), h6: heading(6),
      hr: pick(q(live ? '.markdown-source-view hr' : '.markdown-preview-view hr'), ['border-top-width', 'border-top-color']),
      mark: pick(q(live ? '.cm-highlight' : '.markdown-preview-view mark'), T),
      link: pick(q(live ? '.cm-hmd-internal-link:not(.is-unresolved) .cm-underline' : 'a.internal-link:not(.is-unresolved)'), T),
      unresolved: pick(q(live ? '.is-unresolved .cm-underline' : 'a.is-unresolved'), T),
      inlineCode: pick(q(live ? '.cm-line:not(.HyperMD-codeblock):not(.HyperMD-header) .cm-inline-code:not(.cm-formatting)' : '.markdown-preview-view p code'), [...T, ...B, ...P]),
      codeFrame: pick(q(live ? '.HyperMD-codeblock-begin-bg' : '.markdown-preview-view pre'), ['background-color', ...B]),
      codeText: pick(q(live ? '.cm-line.HyperMD-codeblock:not(.HyperMD-codeblock-begin):not(.HyperMD-codeblock-end)' : '.markdown-preview-view pre code'), T),
      quoteRule: live ? pick(quoteLine, ['border-left-width', 'border-left-color'], '::before')
                      : pick(q('.markdown-preview-view blockquote'), ['border-left-width', 'border-left-color']),
      quoteText: pick(q(live ? '.HyperMD-quote .cm-quote:not(.cm-formatting)' : '.markdown-preview-view blockquote p'), ['color']),
      table: table ? { ...pick(table, ['width', ...B]),
                       parentWidth: `${Math.round(table.closest(live ? '.cm-content' : '.markdown-preview-sizer').getBoundingClientRect().width)}px` } : null,
      th: pick(table?.querySelector('th'), T),
      td: pick(table?.querySelector('td'), T),
      cellPad: pick(live ? table?.querySelector('td .table-cell-wrapper') : table?.querySelector('td'), P),
      tdCode: pick(q(live ? '.cm-table-widget td .cm-inline-code, .cm-table-widget td code' : '.markdown-preview-view td code'), ['font-size']),
      tag: pick(q(live ? '.cm-hashtag.cm-hashtag-end' : 'a.tag'), T),
      calloutNote: pick(q('.callout[data-callout="note"] .callout-title'), ['color']),
      calloutNoteBg: pick(q('.callout[data-callout="note"]'), ['background-color']),
    };
    return Object.fromEntries((SECTION_KEYS[section] || []).map(k => [k, all[k]]));
  }

  // ---- UI probes: detached copies of Obsidian's DOM shapes (file explorer, menu, tooltip,
  // search hits, callouts, tasks…) in an off-screen container. Nothing is inserted into the
  // note or the editor, so the document can never be touched.
  const CALLOUTS = ['note', 'abstract', 'tip', 'success', 'question', 'warning', 'failure', 'danger', 'example', 'quote'];
  const TASKS = ['x', '/', '-', '>', '?', '!'];
  function ensureProbes() {
    let box = document.getElementById('__vprobe');
    if (box) return box;
    box = document.createElement('div');
    box.id = '__vprobe';
    // transform makes this the containing block for fixed-position children (menus), keeping them off-screen
    box.style.cssText = 'position:fixed;top:0;left:0;width:640px;transform:translateX(-20000px);pointer-events:none';
    const item = (cls, probe, text, extra = '') =>
      `<div class="tree-item ${cls.startsWith('nav-folder') ? 'nav-folder is-collapsed' : 'nav-file'}">
         <div class="tree-item-self ${cls} is-clickable${extra}" data-vprobe="${probe}">
           <div class="tree-item-inner ${cls}-content"${probe === 'rename' ? ' contenteditable="true"' : ''}>${text}</div></div></div>`;
    // no transitions inside the probes: a forced :hover must be measured at its end state
    box.innerHTML = `<style>#__vprobe, #__vprobe * { transition: none !important; animation: none !important; }</style>
      <div class="workspace-leaf-content" data-type="file-explorer"><div class="nav-files-container">
        <div class="tree-item nav-folder mod-root">
          <div class="tree-item-self nav-folder-title" data-vprobe="root"><div class="tree-item-inner nav-folder-title-content">vault</div></div>
          <div class="tree-item-children nav-folder-children" data-vprobe="children">
            ${item('nav-folder-title', 'folder', 'folder')}
            ${item('nav-file-title', 'file', 'file')}
            ${item('nav-file-title', 'active', 'active', ' is-active')}
            ${item('nav-file-title', 'rename', 'rename', ' is-being-renamed')}
          </div></div></div></div>
      <div class="menu"><div class="menu-scroll">
        <div class="menu-item" data-vprobe="menu-item"><div class="menu-item-icon">i</div><div class="menu-item-title">Open</div></div>
        <div class="menu-item selected" data-vprobe="menu-sel"><div class="menu-item-icon" data-vprobe="menu-sel-icon">i</div><div class="menu-item-title">Copy</div><div class="menu-item-desc" data-vprobe="menu-sel-desc">desc</div></div>
        <div class="menu-item is-warning selected" data-vprobe="menu-warn"><div class="menu-item-icon" data-vprobe="menu-warn-icon">i</div><div class="menu-item-title">Delete</div></div>
      </div></div>
      <div class="tooltip mod-top" data-vprobe="tooltip"><div class="tooltip-arrow" data-vprobe="tooltip-arrow"></div>tip</div>
      <div class="suggestion-item is-selected" data-vprobe="suggestion"><span class="suggestion-highlight" data-vprobe="suggestion-hl">s</span></div>
      <span class="search-result-file-matched-text" data-vprobe="search-pane">hit</span>
      <div class="cm-s-obsidian"><span class="obsidian-search-match-highlight" data-vprobe="search-edit">m</span>
        <span class="cm-highlight obsidian-search-match-highlight" data-vprobe="search-edit-mark">m</span>
        <span class="cm-hashtag cm-hashtag-end" data-vprobe="hashtag">tag</span></div>
      <div class="markdown-rendered">
        <div class="search-highlight"><div data-vprobe="search-read"></div><div class="is-active" data-vprobe="search-read-active"></div></div>
        ${CALLOUTS.map(c => `<div class="callout" data-callout="${c}" data-vprobe="callout-${c}"><div class="callout-title" data-vprobe="callout-${c}-title">${c}</div></div>`).join('')}
        <ul class="contains-task-list">${TASKS.map((t, i) => `<li class="task-list-item" data-task="${t}" data-vprobe="task-${i}">
          <input type="checkbox" class="task-list-item-checkbox" data-task="${t}" data-vprobe="task-${i}-box">t</li>`).join('')}</ul>
        <p><a class="tag" href="#t" data-vprobe="tag">#t</a> <a class="internal-link" data-vprobe="link">l</a> <mark data-vprobe="mark">m</mark></p>
      </div>
      <div class="prompt" data-vprobe="prompt"><input class="prompt-input" data-vprobe="prompt-input"></div>
      <div class="notice" data-vprobe="notice">n</div>
      <div class="status-bar" data-vprobe="status-bar">s</div>
      <div class="workspace-tab-header is-active" data-vprobe="tab-active">t</div>`;
    document.body.appendChild(box);
    return box;
  }
  const PROBE_PROPS = ['color', 'background-color', 'background-image', 'box-shadow', 'font-weight',
    'border-top-color', 'border-top-width', 'border-left-color', 'border-bottom-color', 'opacity', 'z-index'];
  function probe(id, pseudo) {
    const el = ensureProbes().querySelector(`[data-vprobe="${id}"]`);
    return pick(el, pseudo ? [...PROBE_PROPS, 'content', 'width'] : PROBE_PROPS, pseudo);
  }
  // Every probe in its resting state, plus the resolved Obsidian variables the theme maps.
  function measureUI(varNames) {
    const box = ensureProbes(), out = { vars: {}, probes: {} };
    const bs = getComputedStyle(document.body);
    for (const n of varNames) out.vars[n] = bs.getPropertyValue(n).trim();
    for (const el of box.querySelectorAll('[data-vprobe]')) {
      const id = el.dataset.vprobe;
      out.probes[id] = probe(id);
      if (/^(folder|root|children)$|^task-\d-box$/.test(id)) out.probes[`${id}::before`] = probe(id, '::before');
    }
    out.probes['folder-icon::before'] = pick(box.querySelector('[data-vprobe="folder"] .nav-folder-title-content'), [...PROBE_PROPS, 'content'], '::before');
    return out;
  }
  // used by run.mjs after it forces :hover / :focus-within on a probe through CDP
  function probeState(id) {
    const box = ensureProbes(), el = box.querySelector(`[data-vprobe="${id}"]`);
    return { self: probe(id), icon: pick(el?.querySelector('.nav-folder-title-content'), [...PROBE_PROPS, 'content'], '::before') };
  }
  function removeProbes() { document.getElementById('__vprobe')?.remove(); }

  return { init, variant, viewMode, scrollTo, settle, rect, measure, measureUI, probeState, removeProbes,
           close: () => { removeProbes(); leaf?.detach(); } };
})();
