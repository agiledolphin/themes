// Minimal Chrome DevTools Protocol client for a running Obsidian window.
import fs from 'node:fs';

export async function connect(port) {
  let targets;
  try {
    targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
  } catch {
    throw new Error(`Cannot reach Obsidian's debug port ${port}. Quit Obsidian, then start it with:\n` +
      `  open -a Obsidian --args --remote-debugging-port=${port}`);
  }
  const page = targets.find(t => t.type === 'page');
  if (!page) throw new Error(`No Obsidian window found on port ${port}`);
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.addEventListener('open', res, { once: true }); ws.addEventListener('error', rej, { once: true }); });
  let id = 0;
  const pending = new Map();
  ws.addEventListener('message', e => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  });
  const send = (method, params = {}) => new Promise((res, rej) => {
    const i = ++id;
    pending.set(i, m => (m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result)));
    ws.send(JSON.stringify({ id: i, method, params }));
  });
  // Evaluate an async function body in the page and return its JSON-serializable result.
  const ev = async body => {
    const r = await send('Runtime.evaluate', { expression: `(async () => { ${body} })()`, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || JSON.stringify(r.exceptionDetails));
    return r.result.value;
  };
  const shot = async (path, clip) => {
    const r = await send('Page.captureScreenshot', { format: 'png', ...(clip ? { clip: { scale: 1, ...clip } } : {}) });
    fs.writeFileSync(path, Buffer.from(r.data, 'base64'));
  };
  return { send, ev, shot, close: () => ws.close() };
}
