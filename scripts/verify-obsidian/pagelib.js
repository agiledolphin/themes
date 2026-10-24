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

  function measure() {
    const root = leaf.view.containerEl, live = leaf.view.getMode() !== 'preview';
    // first match that is part of the note itself, not of an embedded note
    const q = s => [...root.querySelectorAll(s)].find(e => !e.closest('.markdown-embed, .internal-embed')) || null;
    const T = ['color', 'font-size', 'font-family', 'line-height', 'background-color'];
    const B = ['border-top-width', 'border-top-color', 'border-left-width', 'border-left-color', 'border-top-left-radius'];
    const P = ['padding-top', 'padding-left', 'padding-right'];
    const table = q(live ? '.cm-table-widget table' : '.markdown-preview-view table');
    const quoteLine = live ? q('.HyperMD-quote') : null;
    const heading = n => pick(q(live ? `.cm-header-${n}` : `.markdown-preview-view h${n}`), T);
    return {
      body: pick(q(live ? '.cm-line' : '.markdown-preview-view p'), T),
      h1: heading(1), h2: heading(2), h3: heading(3), h4: heading(4), h5: heading(5), h6: heading(6),
      hr: pick(q(live ? '.markdown-source-view hr' : '.markdown-preview-view hr'), ['border-top-width', 'border-top-color']),
      mark: pick(q(live ? '.cm-highlight' : '.markdown-preview-view mark'), T),
      link: pick(q(live ? '.cm-hmd-internal-link:not(.is-unresolved) .cm-underline' : 'a.internal-link:not(.is-unresolved)'), T),
      unresolved: pick(q(live ? '.is-unresolved .cm-underline' : 'a.is-unresolved'), T),
      inlineCode: pick(q(live ? '.cm-line:not(.HyperMD-codeblock) .cm-inline-code:not(.cm-formatting)' : '.markdown-preview-view p code'), [...T, ...B, ...P]),
      codeFrame: pick(q(live ? '.HyperMD-codeblock-begin-bg' : '.markdown-preview-view pre'), ['background-color', ...B]),
      codeText: pick(q(live ? '.cm-line.HyperMD-codeblock:not(.HyperMD-codeblock-begin):not(.HyperMD-codeblock-end)' : '.markdown-preview-view pre code'), T),
      quoteRule: live ? pick(quoteLine, ['border-left-width', 'border-left-color'], '::before')
                      : pick(q('.markdown-preview-view blockquote'), ['border-left-width', 'border-left-color']),
      quoteText: pick(q(live ? '.HyperMD-quote .cm-quote:not(.cm-formatting)' : '.markdown-preview-view blockquote p'), ['color']),
      table: table ? { ...pick(table, ['width', ...B]),
                       parentWidth: getComputedStyle(root.querySelector(live ? '.cm-content' : '.markdown-preview-sizer')).width } : null,
      th: pick(table?.querySelector('th'), T),
      td: pick(table?.querySelector('td'), T),
      cellPad: pick(live ? table?.querySelector('td .table-cell-wrapper') : table?.querySelector('td'), P),
      tdCode: pick(q(live ? '.cm-table-widget td .cm-inline-code, .cm-table-widget td code' : '.markdown-preview-view td code'), ['font-size']),
      tag: pick(q(live ? '.cm-hashtag.cm-hashtag-end' : 'a.tag'), T),
      calloutNote: pick(q('.callout[data-callout="note"] .callout-title'), ['color']),
      calloutNoteBg: pick(q('.callout[data-callout="note"]'), ['background-color']),
    };
  }

  return { init, variant, viewMode, scrollTo, rect, measure, close: () => leaf?.detach() };
})();
