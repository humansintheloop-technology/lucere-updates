# {Space}: Regression test (v1.7.5)

Every change to {Name}'s page must pass this before it is published: each Lucere update (os-update-skill.md), each wish or fix built in chat, and each nightly build when the run has a shell with Playwright. It was first built in the first owner's space, at her request, so updates are tested before they reach her.

## What it does
It opens the page from before and the new page in a phone-size browser, twice each: once as a preview with no store, and once live with a pretend store built from the fixture below. The fixture holds no real mail, no names of other people, and no private details. It opens every tab, taps a few safe controls (brief sections, Why on a decision, the Chief's panel), and compares the two pages.

It fails when:
- a page error appears that the page from before didn't have;
- a tab that showed before is gone, or shows less than half as much text as before;
- a feature marker that was on a tab before is gone. The markers are:
  - Today: the hero, the brief, decisions with their buttons, the kids' week, brief sections;
  - Inbox: Search all mail;
  - Calendar: the week arrows;
  - Choices: Write about it and the answer buttons;
  - Trust: the three promises and Updates;
  - Make it yours: notes for chat and the web switch;
- a safe tap causes an error that it didn't cause before.

Size is counted in visible text, not HTML. A redesign that drops icons or wrappers isn't a lost tab. Markers are features, never looks. A wish that changes how Today looks must still pass.

It also saves today-before.png and today-after.png. Look at today-after.png before publishing.

## How to run it
1. Write the two files below exactly: regress.js and fixture.json. Put them in a folder of their own, outside the update's files.
2. Keep the page from before as before.html and the new page as after.html.
3. Run: `NODE_PATH=$(npm root -g) node regress.js before.html after.html fixture.json <outdir>`
4. It must print REGRESSION PASS. On REGRESSION FAIL, don't publish:
   - Change nothing.
   - Tell {Name} in plain words what broke (the lines after REGRESSION FAIL).
   - For an update, leave a note for their chat ("Update v<version> failed its regression test") and offer "Report a problem".
5. If the run has no shell or no Playwright, say so. An update is not applied without this test. A nightly build falls back to the wording-and-color rule in os-nightly-skill.md.

When a new feature is built for them, add its marker to MARKERS in regress.js: a string that is in the tab's HTML only when the feature is there. Then save this doc again.

## regress.js
```js
// Lucere regression test - node regress.js before.html after.html fixture.json [outdir]
// Loads both pages in a phone-size browser: once as a preview (no store), and once live with a pretend store
// built from fixture.json. Opens every tab, taps a few safe controls, and compares after with before.
// FAIL when: a page error appears that before didn't have; a tab shows less than half the text it showed before;
// a feature marker present before is gone now. Writes today-before.png / today-after.png for a visual check.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const [,, BEFORE, AFTER, FIX, OUT = '.'] = process.argv;
const pad = n => String(n).padStart(2, '0'), d = new Date(new Date().toLocaleString('en-US', { timeZone:'America/Chicago' }));
const TODAY = `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
const fixture = JSON.parse(fs.readFileSync(FIX, 'utf8').split('TODAY').join(TODAY));
const MARKERS = {
  today: ['id="t-hero"', 'id="t-brief"', 'id="t-choices"', 'data-act="choose"', 'id="t-kidsweek"', 'data-act="petal"'],
  inbox: ['data-form="msearch"'], calendar: ['id="cal-weeks"'], sc: [], reminders: [], work: [], work2: [], meals: [],
  choices: ['data-act="choice-write"', 'data-act="choose"'], studio: [],
  trust: ['The three promises', 'aria-labelledby="tu-h"'], yours: ['id="y-notes"', 'data-act="web-toggle"'],
};
const MOCK = (data) => {
  const snap = (id, d) => ({ id, exists: d !== undefined, data: () => d, metadata:{ fromCache:false } });
  const docRef = (p) => ({ onSnapshot(cb){ setTimeout(() => cb(snap(p.split('/').pop(), data.docs[p])), 40); return () => {}; },
    set: async () => {}, update: async () => {}, delete: async () => {}, get: async () => snap(p.split('/').pop(), data.docs[p]) });
  const db = { doc: docRef, collection: (n) => ({ onSnapshot(cb){ setTimeout(() => cb({ metadata:{fromCache:false}, docs:(data.cols[n]||[]).map(o => ({ id:o.id, data: () => o })) }), 50); return () => {}; }, doc: (id) => docRef(n + '/' + id) }) };
  const mcp = { callTool: async () => ({ content:[{ type:'text', text:'{}' }] }), servers: async () => [] };
  window.claude = { use: async (n) => n === 'db' ? db : n === 'mcp' ? mcp : n === 'user' ? { canEdit: async () => true } : null };
};
async function run(file, live, shot){
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport:{ width:400, height:900 }, deviceScaleFactor:1, timezoneId:'America/Chicago' });
  const p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  if (live) await p.addInitScript(MOCK, fixture);
  await p.goto('file://' + path.resolve(file)); await p.waitForTimeout(1500);
  const res = { errs, tabs:{} };
  if (shot) await p.screenshot({ path: shot, fullPage: true });
  const tabs = await p.evaluate(() => [...new Set([...document.querySelectorAll('[data-st]')].map(e => e.getAttribute('data-st')))]);
  for (const t of tabs){
    const n0 = errs.length;
    await p.evaluate(t => { const el = document.querySelector(`[data-st="${t}"]`); el && el.click(); }, t);
    await p.waitForTimeout(350);
    const got = await p.evaluate(() => { const m = document.querySelector('#main'); return { html: m ? m.innerHTML : '', text: m ? m.innerText.replace(/\s+/g, ' ').trim() : '' }; });
    /* size is the visible text, not the HTML: a redesign that drops icons or wrappers is not a lost tab */
    res.tabs[t] = { len: got.text.length, markers: (MARKERS[t] || []).filter(m => got.html.includes(m)), errs: errs.slice(n0) };
  }
  // safe taps: brief sections, Chief's panel, a decision's "Why", a choice tab
  const n1 = errs.length;
  await p.evaluate(() => { const go = s => { const el = document.querySelector(s); el && el.click(); };
    go('[data-st="today"]'); go('[data-act="petal-step"][data-i="1"]'); go('[data-act="why"]'); go('[data-act="chief-open"]'); });
  await p.waitForTimeout(500);
  res.taps = errs.slice(n1);
  await b.close(); return res;
}
(async () => {
  const fails = [], rows = [];
  for (const live of [false, true]){
    const mode = live ? 'live' : 'preview';
    const A = await run(BEFORE, live, live ? path.join(OUT, 'today-before.png') : null);
    const B = await run(AFTER, live, live ? path.join(OUT, 'today-after.png') : null);
    const newErr = B.errs.filter(e => !A.errs.includes(e));
    if (newErr.length) fails.push(`${mode}: new page errors: ${newErr.join(' | ')}`);
    for (const t of Object.keys(A.tabs)){
      const a = A.tabs[t], b = B.tabs[t];
      if (!b){ fails.push(`${mode}: tab "${t}" is gone`); continue; }
      const lost = a.markers.filter(m => !b.markers.includes(m));
      if (lost.length) fails.push(`${mode}: tab "${t}" lost ${lost.join(', ')}`);
      if (a.len > 120 && b.len < a.len * 0.5) fails.push(`${mode}: tab "${t}" shrank from ${a.len} to ${b.len}`);
      if (b.errs.length && !a.errs.length) fails.push(`${mode}: tab "${t}" errors: ${b.errs.join(' | ')}`);
      rows.push(`${mode.padEnd(8)} ${t.padEnd(10)} ${String(a.len).padStart(6)} -> ${String(b.len).padStart(6)}  ${b.markers.length}/${(MARKERS[t]||[]).length} markers`);
    }
    if (B.taps.length && !A.taps.length) fails.push(`${mode}: taps caused errors: ${B.taps.join(' | ')}`);
  }
  console.log(rows.join('\n'));
  if (fails.length){ console.log('REGRESSION FAIL\n- ' + fails.join('\n- ')); process.exit(1); }
  console.log('REGRESSION PASS');
})();
```

## fixture.json
TODAY is replaced with today's date (Central time) when the test runs.
```json
{
 "docs": {
  "settings/main": {
   "mode": "live",
   "setupDone": true,
   "setupV": 4,
   "tourDone": true,
   "name": "Sam",
   "space": "Lucere",
   "chief": "Luce",
   "kit_version": "1.7.2",
   "update_channel": "beta",
   "web": true,
   "nightly": true,
   "facets": {
    "family": true,
    "home": true,
    "self": true,
    "work": true,
    "work2": true,
    "sc": true
   },
   "labels": {
    "family": "Family",
    "sc": "Client work",
    "work": "Work",
    "work2": "Side project"
   },
   "kids": [
    "Maya"
   ],
   "restore": [
    {
     "id": "g0",
     "kind": "family",
     "per": 0,
     "t": "More time with Maya"
    },
    {
     "id": "g1",
     "kind": "body",
     "per": 3,
     "t": "Moving my body"
    }
   ],
   "lessOf": [
    "Time on my phone"
   ],
   "calendars": [
    {
     "f": "self",
     "id": "primary",
     "name": "Your main calendar",
     "on": true
    }
   ],
   "keywords": {},
   "priority": "school",
   "stone": "rose",
   "theme": "auto"
  },
  "setup/main": {
   "v": 4,
   "doneAt": 1,
   "tour": true
  },
  "update/main": {
   "latest": "9.9.9",
   "channel": "beta",
   "title": "A test update",
   "note": "Test.",
   "essential": false,
   "versions": [
    "9.9.9"
   ],
   "checkedAt": 1
  },
  "briefs/TODAY": {
   "by": "chief",
   "writtenAt": 1,
   "petals": [
    {
     "k": "shape",
     "h": "The shape of today",
     "lead": "A test day.",
     "items": [
      "One meeting at 10.",
      "An open evening."
     ]
    },
    {
     "k": "needs",
     "h": "What needs you",
     "lead": "One thing.",
     "items": [
      "A test question."
     ]
    },
    {
     "k": "one",
     "h": "If you do one thing",
     "lead": "Rest.",
     "items": []
    }
   ]
  },
  "log/main": {
   "entries": [
    {
     "ts": 1,
     "t": "A test change.",
     "kind": "change",
     "cls": "B",
     "by": "chief",
     "detail": ""
    }
   ]
  }
 },
 "cols": {
  "choices": [
   {
    "id": "c1",
    "a": "family",
    "by": "helper",
    "helperId": "h1",
    "ctx": "Suggested by Inbox Gardener",
    "created": 1794836578151,
    "status": "waiting",
    "rec": 0,
    "options": [
     "Sort it this way",
     "Skip"
    ],
    "why": "A test reason.",
    "q": "Sort yesterday's mail this way? Needs you: Priority: The school's weekly news (Book Fair hours; an optional poll), nothing due. Also Dr. Smith's office confirming Tuesday. Can wait: a bank alert (check it in the app yourself), an order notice, and two shipping notes. Quiet: the other 150 or so (shopping, news)."
   },
   {
    "id": "c2",
    "a": "family",
    "by": "helper",
    "helperId": "h2",
    "ctx": "Suggested by School Notes",
    "created": 1794663763301,
    "status": "waiting",
    "rec": 0,
    "options": [
     "Add the reminder",
     "Skip"
    ],
    "why": "From the school.",
    "act": {
     "kind": "reminder",
     "t": "Sign the field trip form",
     "f": "family",
     "due": "Thu, Nov 19"
    },
    "q": "Add a reminder: Sign the field trip form, due Thu, Nov 19?"
   },
   {
    "id": "c3",
    "a": "work",
    "by": "you",
    "created": 1794663763301,
    "status": "waiting",
    "rec": 1,
    "options": [
     "Tuesday",
     "Thursday"
    ],
    "why": "Thursday is lighter.",
    "q": "Which day for the tasting?",
    "ctx": "Two days are open."
   },
   {
    "id": "c4",
    "a": "self",
    "by": "helper",
    "helperId": "h1",
    "ctx": "Suggested by Inbox Gardener",
    "created": 1794836578151,
    "status": "waiting",
    "rec": 0,
    "options": [
     "Looks right",
     "Not quite"
    ],
    "why": "A test reason.",
    "q": "Does this sort of yesterday's mail look right? Needs you: a form from the school. Can wait: an order notice. Quiet: the other 40 (shopping)."
   }
  ],
  "helpers": [
   {
    "id": "h1",
    "name": "Inbox Gardener",
    "lvl": 0,
    "status": "active",
    "runs": 12,
    "acc": 10
   },
   {
    "id": "h2",
    "name": "School Notes",
    "lvl": 0,
    "status": "active",
    "runs": 10,
    "acc": 6
   }
  ],
  "reminders": [
   {
    "id": "r1",
    "t": "A test reminder",
    "f": "self",
    "due": "Today",
    "dueDate": "TODAY",
    "done": false
   },
   {
    "id": "r2",
    "t": "A family reminder",
    "f": "family",
    "due": "Fri",
    "dueDate": null,
    "done": false
   }
  ],
  "wishes": [
   {
    "id": "w1",
    "t": "A test wish",
    "status": "built",
    "builtBy": "chat",
    "builtAt": 1,
    "note": "Test.",
    "restore": "versions/x.html",
    "created": 1
   }
  ],
  "notes": [
   {
    "id": "n1",
    "t": "A test note.",
    "kind": "idea",
    "by": "brief",
    "status": "open",
    "created": 1
   }
  ],
  "rules": [],
  "recipes": [],
  "choicenotes": []
 }
}
```
