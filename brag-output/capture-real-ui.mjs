import { mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const out = new URL('./assets/real-ui/', import.meta.url);
await mkdir(out, { recursive: true });
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const chromePath = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const profile = fileURLToPath(new URL('./chrome-profile/', import.meta.url));
const { spawn } = await import('node:child_process');
const browser = spawn(chromePath, [
  '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
  '--no-sandbox', '--hide-scrollbars', '--remote-debugging-port=9222',
  `--user-data-dir=${profile}`, '--window-size=1280,1600',
  '--force-device-scale-factor=1', 'http://localhost:5174',
], { stdio: 'ignore', windowsHide: true });

let targets;
for (let attempt = 0; attempt < 40; attempt += 1) {
  try {
    targets = await (await fetch('http://127.0.0.1:9222/json/list')).json();
    if (targets.some((target) => target.type === 'page')) break;
  } catch {}
  await wait(500);
}
const target = targets?.find((item) => item.type === 'page');
if (!target) throw new Error('Chrome remote debugging page did not start.');

const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {
  socket.addEventListener('open', resolve, { once: true });
  socket.addEventListener('error', reject, { once: true });
});
let nextId = 0;
const pending = new Map();
socket.addEventListener('message', async (event) => {
  const raw = typeof event.data === 'string' ? event.data : await event.data.text();
  const data = JSON.parse(raw);
  if (data.id && pending.has(data.id)) {
    const { resolve, reject } = pending.get(data.id);
    pending.delete(data.id);
    if (data.error) reject(new Error(data.error.message));
    else resolve(data.result);
  }
});
const send = (method, params = {}) => new Promise((resolve, reject) => {
  const id = ++nextId;
  pending.set(id, { resolve, reject });
  socket.send(JSON.stringify({ id, method, params }));
});
const evaluate = async (expression, awaitPromise = false) => {
  const response = await send('Runtime.evaluate', {
    expression, awaitPromise, returnByValue: true, userGesture: true,
  });
  if (response.exceptionDetails) throw new Error(response.exceptionDetails.text);
  return response.result?.value;
};
const save = async (name) => {
  const result = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
  await writeFile(new URL(name, out), Buffer.from(result.data, 'base64'));
  process.stdout.write(`${name}\n`);
};
await send('Page.enable');
await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', {
  width: 1280, height: 1600, deviceScaleFactor: 1, mobile: false,
});
await wait(1800);
await evaluate('document.querySelectorAll(".user-badge").forEach((node) => node.remove())');
await save('01-dashboard.png');

const clickText = async (selector, text) => {
  const escaped = JSON.stringify(text);
  const found = await evaluate(`(() => { const el=[...document.querySelectorAll(${JSON.stringify(selector)})].find(x=>x.innerText.includes(${escaped})); if(!el) return false; el.click(); return true })()`);
  if (!found) throw new Error(`Could not find UI control: ${text}`);
  await wait(800);
};
await clickText('.nav-item', 'Weather');
await wait(1200);
await save('02-weather.png');

for (const [file, label] of [
  ['03-crop.png', 'Crop recommendation'],
  ['04-fertilizer.png', 'Fertilizer recommendation'],
  ['05-irrigation.png', 'Irrigation prediction'],
  ['06-price.png', 'Price prediction'],
  ['07-yield.png', 'Yield prediction'],
]) {
  await clickText('.nav-item', 'Overview');
  await clickText('.service-card', label);
  await evaluate('document.querySelector("form.input-card").requestSubmit()');
  for (let attempt = 0; attempt < 100; attempt += 1) {
    const result = await evaluate('document.querySelector(".service-result strong")?.innerText || ""');
    const ready = await evaluate('document.querySelector(".service-result")?.classList.contains("result-ready")');
    if (ready && result && result !== '—') break;
    if (attempt === 99) throw new Error(`Model did not return a result for ${label}.`);
    await wait(200);
  }
  await wait(500);
  await save(file);
}

socket.close();
browser.kill();
