#!/usr/bin/env node
// Drive the running Obsidian through every Lamplit scheme (palette variant) in Reading view
// and Live Preview, screenshot the test note's sections and record computed styles, the
// Obsidian variables the theme sets, and UI probes (file explorer incl. forced :hover,
// menus, tooltips, search hits, callouts, tasks).
//
// Prerequisites
//   - Obsidian started with a debug port:  open -a Obsidian --args --remote-debugging-port=9333
//   - Lamplit synced into the vault:       ./scripts/sync-obsidian.sh ~/notebook
//   - A test note in the vault that has the section headings listed in SECTIONS below.
//
// Usage
//   node scripts/verify-obsidian/run.mjs [--port 9333] [--note <vault path>] [--out .verify] [--only cp-latte,wl]
//   uv run scripts/verify-obsidian/analyze.py .verify [--baseline <other run dir>]
//
// Results are keyed by <palette prefix>-<variant slug> (e.g. cp-latte), so an earlier run can
// serve as --baseline: keep a copy of .verify before a refactor, then compare.
//
// Each run first clears its previous results in --out (screenshots, measure.json, index.html).
// While it runs (~5 min for all variants) Obsidian switches themes on screen — don't use it.
// It works in a new tab, never edits the note, and restores the theme, light/dark mode,
// Style Settings classes and active tab afterwards.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { connect } from './cdp.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const arg = (name, dflt) => { const i = process.argv.indexOf(`--${name}`); return i > 0 ? process.argv[i + 1] : dflt; };
const PORT = arg('port', '9333');
const NOTE = arg('note', 'tech/lab/obsidian/obsidian-theme-sample.md');
const OUT = path.resolve(arg('out', '.verify'));
const ONLY = arg('only', '')?.split(',').filter(Boolean) ?? [];

// [section id, heading text in the test note, screenshot?]
const SECTIONS = [
  ['top', null, true], ['text', 'Text Styles', true], ['tasks', 'Task List', false],
  ['quote-code', 'Blockquotes', true], ['tables', 'Tables', true], ['callouts', 'Callouts', true],
  ['hr', 'Horizontal Rules', false], ['tags', 'Inline Tags', true], ['mermaid', 'Mermaid Diagrams', true],
];

const LAMPLIT_TOML = fs.readFileSync(path.join(ROOT, 'shared/lamplit.toml'), 'utf8');
const LAMPLIT = { name: LAMPLIT_TOML.match(/^name = "(.+)"/m)[1], prefix: LAMPLIT_TOML.match(/^prefix = "(.+?)"/m)[1] };
const MODE = 'lamplit';

// Variants straight from the palette TOMLs (prefix, [[variants]] slug + mode).
function loadVariants() {
  const out = [];
  for (const f of fs.readdirSync(path.join(ROOT, 'shared/palettes')).filter(f => f.endsWith('.toml')).sort()) {
    const text = fs.readFileSync(path.join(ROOT, 'shared/palettes', f), 'utf8');
    const prefix = text.match(/^prefix = "(.+?)"/m)[1];
    for (const block of text.split(/^\[\[variants\]\]$/m).slice(1)) {
      const slug = block.match(/^slug = "(.+?)"/m)[1], mode = block.match(/^mode = "(.+?)"/m)[1];
      const id = `${prefix}-${slug}`;
      out.push({ id, theme: LAMPLIT.name, themeSlug: path.basename(f, '.toml'), mode, cls: `${LAMPLIT.prefix}-${id}` });
    }
  }
  return out;
}

// Obsidian variables the theme sets: the shared `body.theme-dark, body.theme-light` mapping block
// plus any non-palette variables a variant block sets (Lamplit moves style-dependent ones there).
function mappedVarNames() {
  const names = new Set();
  const css = fs.readFileSync(path.join(ROOT, 'obsidian/lamplit/theme.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
  for (const m of css.matchAll(/body\.theme-(?:dark|light)[^{]*\{([^}]*)\}/g))
    for (const n of m[1].matchAll(/(--[a-z0-9-]+)\s*:/g)) if (!n[1].startsWith(`--${LAMPLIT.prefix}-`)) names.add(n[1]);
  return [...names].sort();
}
// [probe id, pseudo-class forced through CDP]
const FORCED = [['file', 'hover'], ['folder', 'hover'], ['active', 'hover'], ['root', 'hover'], ['rename', 'focus-within']];

const all = loadVariants();
const variants = all.filter(v => !ONLY.length || ONLY.some(o => v.id === o || v.id.startsWith(o + '-') || v.themeSlug === o));
if (!variants.length) { console.error(`No variants match --only ${ONLY.join(',')}`); process.exit(2); }

let conn;
try { conn = await connect(PORT); } catch (e) { console.error(e.message); process.exit(2); }
const { ev, send, shot, close } = conn;
// Rendering pauses while the Obsidian window is hidden (minimized, on another Space, covered):
// requestAnimationFrame stops, so lazily rendered content never appears and measurements come
// back empty. Refuse to run — and stop mid-run — rather than record a half-empty result.
class NotRendering extends Error {}
async function assertRendering() {
  const r = await ev(`return await Promise.race([
    new Promise(res => requestAnimationFrame(() => res(document.visibilityState))),
    new Promise(res => setTimeout(() => res('no-frames'), 1500))]);`);
  if (r !== 'visible') {
    throw new NotRendering(`Obsidian's window is not rendering (${r}). Bring it to the front and keep it`
      + ' visible (not minimized, covered or on another Space) for the whole run, then retry.');
  }
}
await ev(fs.readFileSync(path.join(HERE, 'pagelib.js'), 'utf8') + '; return 1;');
const orig = await ev(`return { theme: app.customCss.theme, mode: app.vault.getConfig('theme'),
  classes: [...document.body.classList], leafId: app.workspace.getMostRecentLeaf()?.id };`);
const variantClasses = all.map(v => v.cls);
try { await assertRendering(); } catch (e) { console.error(e.message); close(); process.exit(3); }
// Connected and rendering — now start from a clean slate so a report never mixes in screenshots from an earlier run.
// Only this tool's own outputs are removed; anything else in OUT is left alone.
fs.mkdirSync(path.join(OUT, 'shots'), { recursive: true });
for (const f of fs.readdirSync(path.join(OUT, 'shots'))) if (f.endsWith('.png')) fs.rmSync(path.join(OUT, 'shots', f));
for (const f of ['measure.json', 'index.html']) fs.rmSync(path.join(OUT, f), { force: true });
const varNames = mappedVarNames();
let completed = false, failure = null;
const results = { note: NOTE, mode: MODE, variants: variants.map(v => ({ ...v })), data: {}, ui: {} };
try {
  const lines = await ev(`return await __V.init(${JSON.stringify({ note: NOTE, variantClasses })});`);
  const sections = SECTIONS.filter(([id, h]) => {
    if (h && lines[h] === undefined) { console.warn(`  (skipping section "${id}": heading "${h}" not in note)`); return false; }
    return true;
  }).map(([id, h, s]) => [id, h, h ? lines[h] : 0, s]);
  await send('DOM.enable'); await send('CSS.enable');
  for (const v of variants) {
    await assertRendering();
    await ev(`await __V.variant(${JSON.stringify(v.theme)}, '${v.mode}', '${v.cls}'); return 1;`);
    const ui = await ev(`return __V.measureUI(${JSON.stringify(varNames)});`);
    ui.states = {};
    for (const [id, pseudo] of FORCED) {
      const { root } = await send('DOM.getDocument', { depth: 1 });
      const { nodeId } = await send('DOM.querySelector', { nodeId: root.nodeId, selector: `[data-vprobe="${id}"]` });
      await send('CSS.forcePseudoState', { nodeId, forcedPseudoClasses: [pseudo] });
      await new Promise(r => setTimeout(r, 60));
      ui.states[`${id}:${pseudo}`] = await ev(`return __V.probeState('${id}');`);
      await send('CSS.forcePseudoState', { nodeId, forcedPseudoClasses: [] });
    }
    results.ui[v.id] = ui;
    for (const view of ['reading', 'live']) {
      await ev(`await __V.viewMode('${view}'); return 1;`);
      const merged = {};
      for (const [id, heading, line, takeShot] of sections) {
        await ev(`await __V.scrollTo(${line}, ${JSON.stringify(heading)}); await __V.settle(${JSON.stringify(id)}); return 1;`);
        const m = await ev(`return __V.measure(${JSON.stringify(id)});`);
        for (const [k, val] of Object.entries(m)) if (merged[k] == null && val != null) merged[k] = val;
        if (takeShot) await shot(path.join(OUT, 'shots', `${v.id}-${view}-${id}.png`), { ...(await ev('return __V.rect();')), scale: 0.35 });
      }
      results.data[`${v.id}/${view}`] = merged;
      process.stdout.write(`${v.id}/${view} `);
    }
  }
  completed = true;
} catch (e) {
  if (!(e instanceof NotRendering)) throw e;
  failure = e.message;
} finally {
  await ev(`__V.close();
    if (app.customCss.theme !== ${JSON.stringify(orig.theme)}) { app.customCss.setTheme(${JSON.stringify(orig.theme)}); await new Promise(r => setTimeout(r, 900)); }
    if (app.vault.getConfig('theme') !== ${JSON.stringify(orig.mode)}) app.changeTheme(${JSON.stringify(orig.mode)});
    await new Promise(r => setTimeout(r, 500));
    const keep = new Set(${JSON.stringify(orig.classes)});
    ${JSON.stringify(variantClasses)}.forEach(c => document.body.classList.toggle(c, keep.has(c)));
    const back = app.workspace.getLeafById(${JSON.stringify(orig.leafId)}); if (back) app.workspace.setActiveLeaf(back, { focus: true });
    return 1;`).catch(e => console.error('\nRESTORE FAILED — check Obsidian\'s theme settings:', e.message));
  if (completed) fs.writeFileSync(path.join(OUT, 'measure.json'), JSON.stringify(results, null, 1));
  close();
}
if (failure) { console.error(`\n${failure}\n(Obsidian restored to ${orig.theme}; no results written.)`); process.exit(3); }
console.log(`\nRestored Obsidian to ${orig.theme} (${orig.mode}). Results: ${path.relative(process.cwd(), OUT)}/measure.json`);
