#!/usr/bin/env node
// Drive the running Obsidian through every theme variant in Reading view and
// Live Preview, screenshot the test note's sections and record computed styles.
//
// Prerequisites
//   - Obsidian started with a debug port:  open -a Obsidian --args --remote-debugging-port=9333
//   - The themes synced into the vault:    ./scripts/sync-obsidian.sh ~/notebook
//   - A test note in the vault that has the section headings listed in SECTIONS below.
//
// Usage
//   node scripts/verify-obsidian/run.mjs [--port 9333] [--note <vault path>] [--out .verify] [--only cp-latte,wl]
//   uv run scripts/verify-obsidian/analyze.py .verify       # report + exit 1 on Reading/Live mismatches
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
  ['hr', 'Horizontal Rules', false], ['tags', 'Inline Tags', true],
];

// Variants straight from the theme TOMLs (theme name, prefix, [[variants]] slug + mode).
function loadVariants() {
  const out = [];
  for (const f of fs.readdirSync(path.join(ROOT, 'shared/palettes')).filter(f => f.endsWith('.toml')).sort()) {
    const text = fs.readFileSync(path.join(ROOT, 'shared/palettes', f), 'utf8');
    const name = text.match(/^name = "(.+)"/m)[1], prefix = text.match(/^prefix = "(.+?)"/m)[1];
    for (const block of text.split(/^\[\[variants\]\]$/m).slice(1)) {
      const slug = block.match(/^slug = "(.+?)"/m)[1], mode = block.match(/^mode = "(.+?)"/m)[1];
      out.push({ theme: name, themeSlug: path.basename(f, '.toml'), mode, cls: `${prefix}-${slug}` });
    }
  }
  return out;
}

const all = loadVariants();
const variants = all.filter(v => !ONLY.length || ONLY.some(o => v.cls === o || v.cls.startsWith(o + '-') || v.themeSlug === o));
if (!variants.length) { console.error(`No variants match --only ${ONLY.join(',')}`); process.exit(2); }

let conn;
try { conn = await connect(PORT); } catch (e) { console.error(e.message); process.exit(2); }
const { ev, shot, close } = conn;
// Connected — now start from a clean slate so a report never mixes in screenshots from an earlier run.
// Only this tool's own outputs are removed; anything else in OUT is left alone.
fs.mkdirSync(path.join(OUT, 'shots'), { recursive: true });
for (const f of fs.readdirSync(path.join(OUT, 'shots'))) if (f.endsWith('.png')) fs.rmSync(path.join(OUT, 'shots', f));
for (const f of ['measure.json', 'index.html']) fs.rmSync(path.join(OUT, f), { force: true });
await ev(fs.readFileSync(path.join(HERE, 'pagelib.js'), 'utf8') + '; return 1;');
const orig = await ev(`return { theme: app.customCss.theme, mode: app.vault.getConfig('theme'),
  classes: [...document.body.classList], leafId: app.workspace.getMostRecentLeaf()?.id };`);
const variantClasses = all.map(v => v.cls);
const results = { note: NOTE, variants: variants.map(v => ({ ...v })), data: {} };
try {
  const lines = await ev(`return await __V.init(${JSON.stringify({ note: NOTE, variantClasses })});`);
  const sections = SECTIONS.filter(([id, h]) => {
    if (h && lines[h] === undefined) { console.warn(`  (skipping section "${id}": heading "${h}" not in note)`); return false; }
    return true;
  }).map(([id, h, s]) => [id, h, h ? lines[h] : 0, s]);
  for (const v of variants) {
    await ev(`await __V.variant(${JSON.stringify(v.theme)}, '${v.mode}', '${v.cls}'); return 1;`);
    for (const view of ['reading', 'live']) {
      await ev(`await __V.viewMode('${view}'); return 1;`);
      const merged = {};
      for (const [id, heading, line, takeShot] of sections) {
        await ev(`await __V.scrollTo(${line}, ${JSON.stringify(heading)}); return 1;`);
        const m = await ev('return __V.measure();');
        for (const [k, val] of Object.entries(m)) if (merged[k] == null && val != null) merged[k] = val;
        if (takeShot) await shot(path.join(OUT, 'shots', `${v.cls}-${view}-${id}.png`), { ...(await ev('return __V.rect();')), scale: 0.35 });
      }
      results.data[`${v.cls}/${view}`] = merged;
      process.stdout.write(`${v.cls}/${view} `);
    }
  }
} finally {
  await ev(`__V.close();
    if (app.customCss.theme !== ${JSON.stringify(orig.theme)}) { app.customCss.setTheme(${JSON.stringify(orig.theme)}); await new Promise(r => setTimeout(r, 900)); }
    if (app.vault.getConfig('theme') !== ${JSON.stringify(orig.mode)}) app.changeTheme(${JSON.stringify(orig.mode)});
    await new Promise(r => setTimeout(r, 500));
    const keep = new Set(${JSON.stringify(orig.classes)});
    ${JSON.stringify(variantClasses)}.forEach(c => document.body.classList.toggle(c, keep.has(c)));
    const back = app.workspace.getLeafById(${JSON.stringify(orig.leafId)}); if (back) app.workspace.setActiveLeaf(back, { focus: true });
    return 1;`).catch(e => console.error('\nRESTORE FAILED — check Obsidian\'s theme settings:', e.message));
  fs.writeFileSync(path.join(OUT, 'measure.json'), JSON.stringify(results, null, 1));
  close();
}
console.log(`\nRestored Obsidian to ${orig.theme} (${orig.mode}). Results: ${path.relative(process.cwd(), OUT)}/measure.json`);
