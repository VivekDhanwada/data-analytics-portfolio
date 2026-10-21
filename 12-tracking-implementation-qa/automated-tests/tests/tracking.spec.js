const { test, expect } = require('@playwright/test');
const spec = require('./event-spec');

// ---------- helpers ----------

// Turn one /g/collect request into a list of flat parameter maps.
function parseCollect(req) {
  const base = {};
  new URL(req.url()).searchParams.forEach((v, k) => { base[k] = v; });
  const body = req.postData();
  const lines = body ? body.split('\n').filter(Boolean) : [];
  if (!lines.length) { return [base]; }
  return lines.map((line) => {
    const m = Object.assign({}, base);
    new URLSearchParams(line).forEach((v, k) => { m[k] = v; });
    return m;
  });
}

// GA4 sends custom parameters as ep.<name> (text) and epn.<name> (number).
function toEvent(m) {
  const params = {};
  Object.keys(m).forEach((k) => {
    if (k.indexOf('epn.') === 0) { params[k.slice(4)] = Number(m[k]); }
    else if (k.indexOf('ep.') === 0) { params[k.slice(3)] = m[k]; }
  });
  return { name: m.en, params };
}

const layerEvents = (page, name) =>
  page.evaluate((n) => (window.dataLayer || []).filter((e) => e && e.event === n), name);

// Layer 1: the dataLayer push matches the event specification.
function assertSpec(name, payload) {
  const fields = spec[name];
  Object.keys(fields).forEach((key) => {
    expect(payload[key], name + ': ' + key + ' is missing from the push').toBeDefined();
    expect(typeof payload[key], name + ': ' + key + ' has the wrong type').toBe(fields[key]);
    if (fields[key] === 'string') {
      expect(payload[key].length, name + ': ' + key + ' is empty').toBeGreaterThan(0);
    }
  });
  if (fields.link_location) {
    expect(spec.LINK_LOCATIONS, name + ': unexpected link_location').toContain(payload.link_location);
  }
}

// Layer 2: the outgoing GA4 request carries the same values as the push.
async function assertRequest(page, name, payload) {
  await expect
    .poll(() => page.collected.map(toEvent).filter((e) => e.name === name).length, { timeout: 10000 })
    .toBeGreaterThan(0);
  const sent = page.collected.map(toEvent).filter((e) => e.name === name).pop();
  Object.keys(spec[name]).forEach((key) => {
    expect(sent.params[key], name + ': ' + key + ' never reached GA4').toBeDefined();
    expect(String(sent.params[key]), name + ': ' + key + ' differs in the GA4 request').toBe(String(payload[key]));
  });
}

async function expectEvent(page, name) {
  await expect.poll(async () => (await layerEvents(page, name)).length).toBeGreaterThan(0);
  const all = await layerEvents(page, name);
  const payload = all[all.length - 1];
  assertSpec(name, payload);
  await assertRequest(page, name, payload);
  return payload;
}

// Mark the first link whose href matches, so the test can click it.
async function markLink(page, key, pattern) {
  const found = await page.evaluate(([k, src]) => {
    const re = new RegExp(src, 'i');
    const a = Array.from(document.querySelectorAll('a[href]')).find((x) => re.test(x.href));
    if (a) { a.setAttribute('data-qa', k); }
    return !!a;
  }, [key, pattern]);
  expect(found, 'no link matching ' + pattern + ' on this page').toBe(true);
  return page.locator('[data-qa="' + key + '"]').first();
}

// ---------- setup ----------

test.beforeEach(async ({ page }) => {
  page.collected = [];
  // Stop links navigating away, after tracking.js (capture phase) has run.
  await page.addInitScript(() => {
    document.addEventListener('click', (e) => {
      if (e.target && e.target.closest && e.target.closest('a[href]')) { e.preventDefault(); }
    }, false);
  });
  // Record GA4 requests and answer them locally, so no test data reaches GA4.
  await page.route('**/g/collect*', async (route) => {
    parseCollect(route.request()).forEach((m) => page.collected.push(m));
    await route.fulfill({ status: 204, body: '' });
  });
});

// ---------- tests ----------

test('resume_download', async ({ page }) => {
  await page.goto('/?internal=1');
  await (await markLink(page, 'resume', '/resume\\.pdf$')).click();
  const p = await expectEvent(page, 'resume_download');
  expect(p.file_name).toBe('resume.pdf');
});

test('project_click from the landing page', async ({ page }) => {
  await page.goto('/?internal=1');
  await page.locator('a.project-row-card').first().click();
  const p = await expectEvent(page, 'project_click');
  expect(p.link_location).toBe('landing_card');
});

test('project_click from the projects index', async ({ page }) => {
  await page.goto('/projects/?internal=1');
  await page.locator('a.project.card').first().click();
  const p = await expectEvent(page, 'project_click');
  expect(p.link_location).toBe('projects_index');
});

const contacts = [
  ['email', '^mailto:'],
  ['linkedin', 'linkedin\\.com/in/vivek-dhanwada/?$'],
  ['github', '^https://github\\.com/vivekdhanwada/?$'],
];
contacts.forEach(([method, pattern]) => {
  test('contact_click: ' + method, async ({ page }) => {
    await page.goto('/?internal=1');
    await (await markLink(page, 'contact', pattern)).click();
    const p = await expectEvent(page, 'contact_click');
    expect(p.contact_method).toBe(method);
  });
});

test('outbound_click drops the query string and keeps the domain', async ({ page }) => {
  await page.goto('/projects/tracking-case-study?internal=1');
  await (await markLink(page, 'repo', 'github\\.com/vivekdhanwada/data-analytics-portfolio')).click();
  const p = await expectEvent(page, 'outbound_click');
  expect(p.link_domain).toBe('github.com');
  expect(p.link_url).not.toContain('?');
  expect(p.link_location).toBe('page_body');
});

test('an internal link is not tracked as outbound', async ({ page }) => {
  await page.goto('/?internal=1');
  const found = await page.evaluate(() => {
    const a = Array.from(document.querySelectorAll('.navbar a[href]')).find(
      (x) => x.hostname === location.hostname && !/resume\.pdf$/i.test(x.pathname));
    if (a) { a.setAttribute('data-qa', 'internal'); }
    return !!a;
  });
  expect(found, 'no internal navbar link found').toBe(true);
  await page.locator('[data-qa="internal"]').first().click();
  await page.waitForTimeout(1000);
  expect(await layerEvents(page, 'outbound_click')).toHaveLength(0);
});

test('scroll_depth fires 25, 50, 75, 100 once each per page load', async ({ page }) => {
  await page.goto('/projects/tracking-case-study?internal=1');
  const scrollTo = async (fraction) => {
    await page.evaluate((f) => {
      const d = document.documentElement;
      window.scrollTo(0, (d.scrollHeight - window.innerHeight) * f);
    }, fraction);
    await page.waitForTimeout(300);
  };
  for (const f of [0.3, 0.55, 0.8, 1]) { await scrollTo(f); }

  await expect.poll(async () => (await layerEvents(page, 'scroll_depth')).length).toBe(4);
  const depths = (await layerEvents(page, 'scroll_depth')).map((e) => e.depth_percent);
  expect(depths).toEqual([25, 50, 75, 100]);
  (await layerEvents(page, 'scroll_depth')).forEach((e) => assertSpec('scroll_depth', e));
  await assertRequest(page, 'scroll_depth', (await layerEvents(page, 'scroll_depth')).pop());

  // Scrolling up and down again must not fire anything new.
  await scrollTo(0);
  await scrollTo(1);
  expect(await layerEvents(page, 'scroll_depth')).toHaveLength(4);
});
