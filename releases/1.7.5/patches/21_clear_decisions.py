"""Lucere v1.7.5 (beta): each decision is its own clear card, in plain words.
On top, the part of life and who suggested it; then a plain title. A mail sort reads "Your mail from <day>,
sorted", with Needs you, Can wait, and a quiet line, long lists folded under "+ N more". A reminder reads
"Add this to your reminders?" with the reminder large and its due date. Buttons say what they mean
("Yes, looks right" / "Not quite", "Yes, add it" / "No, skip it"). Display only: stored choices, their
options, and what each answer does are unchanged. Reads both mail-sort wordings ("Sort yesterday's mail
this way?" and the kit's "Does this sort of yesterday's mail look right?"). Raises the page's version to 1.7.5.
Run: python3 21_clear_decisions.py in.html out.html"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, 'expected one match (found %d) for: %s' % (n, old[:60])
    s = s.replace(old, new)


rep("const KIT_VERSION = '1.7.4';",
    "const KIT_VERSION = '1.7.5';")

rep((
    '</style>\n'
    '\n'
    '<div class="opal" aria-hidden="true"></div>'
),
    (
    '/* ---------- Decisions: one clear card each (Lucere v1.7.5) ---------- */\n'
    '.choice.dec{border:0; padding:20px 22px 18px; margin:0 0 14px; background:var(--surface);\n'
    '  border-radius:26px 14px 28px 16px; box-shadow:inset 4px 0 0 var(--area, var(--accent)), 0 1px 2px hsl(var(--h) 30% 25% / .05), 0 14px 30px -22px hsl(var(--h) 40% 30% / .4)}\n'
    '.choice.dec:first-of-type{padding-top:20px}\n'
    '.choice.dec:last-child{margin-bottom:0}\n'
    '.dec-top{display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap; font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); margin-bottom:8px}\n'
    '.dec-tag{display:inline-flex; align-items:center; gap:7px}\n'
    '.dec-title{font-family:var(--f-serif); font-size:23px; font-weight:500; line-height:1.2; margin:0 0 12px; color:var(--ink); text-wrap:pretty}\n'
    '.dec-group{margin:0 0 8px}\n'
    '.dec-gh{font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--accent-ink); font-weight:500; margin:0 0 2px}\n'
    '.dec-group.later .dec-gh{color:var(--muted)}\n'
    '.dec ul{list-style:none; margin:0; padding:0}\n'
    '.dec li{position:relative; padding:5px 0 5px 16px; font-size:15px; line-height:1.45; overflow-wrap:anywhere}\n'
    '.dec li::before{content:""; position:absolute; left:2px; top:13px; width:6px; height:6px; border-radius:50%; background:var(--area, var(--accent)); opacity:.65}\n'
    '.dec .pri{display:inline-block; font-size:9.5px; letter-spacing:.12em; text-transform:uppercase; background:var(--accent-soft); color:var(--accent-ink); padding:2px 8px; border-radius:999px; margin-right:6px; vertical-align:2px}\n'
    '.dec details > summary{cursor:pointer; color:var(--accent-ink); font-size:14px; padding:4px 0 2px 16px; list-style:none}\n'
    '.dec details > summary::-webkit-details-marker{display:none}\n'
    '.dec-quiet{font-size:14px; color:var(--muted); margin:6px 0 0; line-height:1.45}\n'
    '.dec-big{font-size:19px; line-height:1.4; margin:0 0 10px; font-weight:500}\n'
    '.dec-due{display:inline-flex; align-items:center; gap:6px; font-size:13px; padding:5px 12px; border-radius:999px; background:var(--accent-soft); color:var(--accent-ink)}\n'
    '.dec-ask{font-weight:500; margin:16px 0 10px; font-size:16px}\n'
    '.dec-btns{gap:10px}\n'
    '.dec-btns .btn{min-width:124px}\n'
    '.dec-note{font-size:13px; color:var(--muted); margin:10px 0 0}\n'
    '.dec-links{margin-top:8px; gap:18px}\n'
    '.dec .why{font-size:17px}\n'
    '</style>\n'
    '\n'
    '<div class="opal" aria-hidden="true"></div>'
))

rep((
    'function choiceHTML(c){\n'
    '  const said = choiceSaid(c.id), saidHTML = said ? `<p class="said"><span>Your note</span>${esc(said)}</p>` : \'\';\n'
    "  if (c.status === 'done'){\n"
    '    return `<div class="choice"><div class="decided"><div><div class="q">${esc(c.q)}</div><p class="ctx" style="margin:4px 0 0">${c.did && c.did.kind === \'reminder\' ? \'Added to your reminders.\' : `You chose <b>${esc((c.options || [])[c.answer] || \'\')}</b>.`}</p></div><button type="button" class="link small" data-act="choice-reopen" data-id="${esc(c.id)}">Reopen</button></div>${saidHTML}</div>`;\n'
    '  }\n'
    '  const open = whyOpen[c.id], wr = !!writeOpen[c.id];\n'
    '  return `<div class="choice" style="--area:var(${AREA[c.a] || \'--accent\'})">\n'
    '    <div class="q"><span class="dot"></span>${esc(c.q)}</div>\n'
    '    ${c.ctx ? `<p class="ctx">${esc(c.ctx)}</p>` : \'<p class="ctx"></p>\'}\n'
    '    ${c.helperId ? `<p class="ctx small muted">${helperAct(c) ? `Yes does this one thing, with an undo, and teaches ${esc(helperName(c))}.` : `Your answer teaches ${esc(helperName(c))}. Nothing else changes.`}</p>` : \'\'}\n'
    '    <div class="row">${(c.options || []).map((o,i) => `<button type="button" class="chip opt${i === c.rec ? \' rec\' : \'\'}" data-act="choose" data-id="${esc(c.id)}" data-i="${i}">${i === c.rec ? gem() : \'\'}${esc(o)}${i === c.rec ? \' <span class="reclbl">Recommended</span>\' : \'\'}</button>`).join(\'\')}</div>\n'
    '    <div class="row" style="margin-top:10px">\n'
    '      <button type="button" class="link small" data-act="why" data-id="${esc(c.id)}" aria-expanded="${!!open}">${open ? \'Hide the reason\' : \'Why this?\'}</button>\n'
    '      <button type="button" class="link small" data-act="choice-write" data-id="${esc(c.id)}" aria-expanded="${wr}">${wr ? \'Close\' : \'Write about it\'}</button>\n'
    '      ${c.status === \'waiting\' ? `<button type="button" class="link small" data-act="choice-later" data-id="${esc(c.id)}">Later</button>` : `<button type="button" class="link small" data-act="choice-reopen" data-id="${esc(c.id)}">Move to waiting</button>`}\n'
    '    </div>'
),
    (
    '/* Decisions in plain words (Lucere v1.7.5). Display only: the stored choice, its options, and what each answer does are unchanged. */\n'
    'const DEC_ABBR = /(?:^|\\s)(?:Dr|Mr|Mrs|Ms|St|Jr|Sr|Mt|vs|No|U\\.S|e\\.g|i\\.e)$/;\n'
    'function decSplit(t, seps){\n'
    "  const out = []; let depth = 0, cur = '';\n"
    '  for (let i = 0; i < t.length; i++){\n'
    '    const ch = t[i];\n'
    "    if (ch === '(') depth++; else if (ch === ')') depth = Math.max(0, depth - 1);\n"
    '    if (!depth){\n'
    "      if (seps.includes(';') && ch === ';'){ out.push(cur); cur = ''; continue; }\n"
    "      if (seps.includes(',') && ch === ','){ out.push(cur); cur = ''; continue; }\n"
    "      if (seps.includes('.') && ch === '.' && t[i+1] === ' ' && /[A-Z]/.test(t[i+2] || '') && !DEC_ABBR.test(cur) && !/(?:^|\\s)[A-Z]$/.test(cur)){ out.push(cur); cur = ''; continue; }\n"
    '    }\n'
    '    cur += ch;\n'
    '  }\n'
    '  out.push(cur);\n'
    "  return out.map(x => x.trim().replace(/^(?:also|and)\\s+/i, '').replace(/\\.+$/, '').trim()).filter(Boolean).map(x => x.charAt(0).toUpperCase() + x.slice(1));\n"
    '}\n'
    'function decKind(c){\n'
    "  if (/^\\s*(?:sort yesterday['\u2019]?s mail this way|does this sort of yesterday['\u2019]?s mail look right)\\?/i.test(String(c.q || ''))) return 'mail';\n"
    "  if (helperAct(c)) return 'rem';\n"
    "  return 'gen';\n"
    '}\n'
    'function decMail(q){\n'
    "  const t = String(q || '').replace(/^\\s*(?:sort yesterday['\u2019]?s mail this way|does this sort of yesterday['\u2019]?s mail look right)\\?\\s*/i, '');\n"
    '  const rx = /(Needs you|Can wait|Quiet)\\s*:\\s*/g, marks = []; let m;\n'
    '  while ((m = rx.exec(t))) marks.push({ k:m[1], i:m.index, j:rx.lastIndex });\n'
    "  const out = { needs:'', wait:'', quiet:'' };\n"
    '  if (!marks.length){ out.needs = t; return out; }\n'
    "  marks.forEach((mk, n) => { const end = n + 1 < marks.length ? marks[n+1].i : t.length, key = mk.k === 'Needs you' ? 'needs' : mk.k === 'Can wait' ? 'wait' : 'quiet'; out[key] = t.slice(mk.j, end).trim().replace(/\\.+$/, ''); });\n"
    '  return out;\n'
    '}\n'
    "function decDay(ms, back){ if (!ms) return ''; const d = new Date(ms); if (back) d.setDate(d.getDate() - back); return d.toLocaleDateString([], { weekday:'short', month:'short', day:'numeric' }); }\n"
    'function decItem(x){ const p = x.match(/^Priority\\s*:\\s*(.+)$/i); return `<li>${p ? `<span class="pri">Priority</span>${esc(p[1])}` : esc(x)}</li>`; }\n'
    'function decList(items, keep){\n'
    "  if (!items.length) return '';\n"
    '  const head = items.slice(0, keep), rest = items.slice(keep);\n'
    "  return `<ul>${head.map(decItem).join('')}</ul>${rest.length ? `<details><summary>+ ${rest.length} more</summary><ul>${rest.map(decItem).join('')}</ul></details>` : ''}`;\n"
    '}\n'
    'function decTitle(c){\n'
    '  const k = decKind(c);\n'
    "  if (k === 'mail') return c.created ? `Your mail from ${decDay(c.created, 1)}, sorted` : 'Yesterday\u2019s mail, sorted';\n"
    "  if (k === 'rem') return 'Add this to your reminders?';\n"
    "  return String(c.q || '');\n"
    '}\n'
    'function decOpt(c, o){\n'
    "  const k = decKind(c), t = String(o || '');\n"
    "  if (k === 'mail'){ if (/^(?:sort it this way|looks right)$/i.test(t)) return 'Yes, looks right'; if (/^skip$/i.test(t)) return 'Not quite'; }\n"
    "  if (k === 'rem'){ if (/^add (?:the|a|this)? ?reminder$/i.test(t)) return 'Yes, add it'; if (/^skip$/i.test(t)) return 'No, skip it'; }\n"
    '  return t;\n'
    '}\n'
    'function choiceHTML(c){\n'
    '  const said = choiceSaid(c.id), saidHTML = said ? `<p class="said"><span>Your note</span>${esc(said)}</p>` : \'\';\n'
    "  const k = decKind(c), area = `--area:var(${AREA[c.a] || '--accent'})`;\n"
    "  if (c.status === 'done'){\n"
    '    return `<div class="choice dec" style="${area}"><div class="decided"><div><div class="dec-title" style="font-size:19px; margin:0">${esc(decTitle(c))}</div>${k === \'rem\' ? `<p class="ctx" style="margin:4px 0 0">${esc(helperAct(c).t)}</p>` : \'\'}<p class="ctx" style="margin:4px 0 0">${c.did && c.did.kind === \'reminder\' ? \'Added to your reminders.\' : `You chose <b>${esc(decOpt(c, (c.options || [])[c.answer] || \'\'))}</b>.`}</p></div><button type="button" class="link small" data-act="choice-reopen" data-id="${esc(c.id)}">Reopen</button></div>${saidHTML}</div>`;\n'
    '  }\n'
    '  const open = whyOpen[c.id], wr = !!writeOpen[c.id];\n'
    "  const from = c.helperId ? `From ${esc(helperName(c))}` : c.by === 'chief' ? `From ${esc(S.chief)}` : '';\n"
    "  let body = '', ask = '', note = '';\n"
    "  if (k === 'mail'){\n"
    "    const M = decMail(c.q), needs = decSplit(M.needs, [';', '.']), wait = decSplit(M.wait, [',', ';']);\n"
    '    const nothing = !needs.length || (needs.length === 1 && /^nothing/i.test(needs[0]));\n'
    '    body = `<div class="dec-group"><p class="dec-gh">Needs you</p>${nothing ? `<p class="dec-quiet" style="margin:2px 0 0">${esc(needs[0] || \'Nothing new.\')}</p>` : decList(needs, 6)}</div>\n'
    '      ${wait.length ? `<div class="dec-group later"><p class="dec-gh">Can wait</p>${decList(wait, 3)}</div>` : \'\'}\n'
    '      ${M.quiet ? `<p class="dec-quiet">Everything else is quiet: ${esc(M.quiet.replace(/^the other\\s+/i, \'about \').replace(/^about about/i, \'about\'))}.</p>` : \'\'}`;\n'
    "    ask = 'Does this sorting look right?';\n"
    '    note = `Your answer helps ${esc(helperName(c))} learn. Nothing else changes.`;\n'
    "  } else if (k === 'rem'){\n"
    '    const A = helperAct(c);\n'
    '    body = `<p class="dec-big">${esc(A.t.charAt(0).toUpperCase() + A.t.slice(1))}</p>${A.due ? `<span class="dec-due">Due ${esc(A.due)}</span>` : \'\'}`;\n'
    "    note = 'Yes adds it to your reminders. You can undo it.';\n"
    '  } else {\n'
    '    body = c.ctx && !/^suggested by/i.test(c.ctx) ? `<p class="ctx" style="margin:0 0 4px">${esc(c.ctx)}</p>` : \'\';\n'
    '    if (c.helperId) note = `Your answer helps ${esc(helperName(c))} learn. Nothing else changes.`;\n'
    '  }\n'
    '  return `<div class="choice dec" style="${area}">\n'
    '    <div class="dec-top"><span class="dec-tag"><span class="dot"></span>${esc(lab(c.a || \'self\'))}${from ? ` \xb7 ${from}` : \'\'}</span>${c.created ? `<span>${esc(decDay(c.created))}</span>` : \'\'}</div>\n'
    '    <p class="dec-title">${esc(decTitle(c))}</p>\n'
    '    ${body}\n'
    '    ${ask ? `<p class="dec-ask">${esc(ask)}</p>` : \'<div style="height:14px"></div>\'}\n'
    '    <div class="row dec-btns">${(c.options || []).map((o,i) => `<button type="button" class="btn${i === c.rec ? \'\' : \' ghost\'} opt${i === c.rec ? \' rec\' : \'\'}" data-act="choose" data-id="${esc(c.id)}" data-i="${i}">${esc(decOpt(c, o))}</button>`).join(\'\')}</div>\n'
    '    ${note ? `<p class="dec-note">${note}</p>` : \'\'}\n'
    '    <div class="row dec-links">\n'
    '      ${c.why ? `<button type="button" class="link small" data-act="why" data-id="${esc(c.id)}" aria-expanded="${!!open}">${open ? \'Hide the reason\' : \'Why I suggest this\'}</button>` : \'\'}\n'
    '      <button type="button" class="link small" data-act="choice-write" data-id="${esc(c.id)}" aria-expanded="${wr}">${wr ? \'Close\' : \'Write about it\'}</button>\n'
    '      ${c.status === \'waiting\' ? `<button type="button" class="link small" data-act="choice-later" data-id="${esc(c.id)}">Later</button>` : `<button type="button" class="link small" data-act="choice-reopen" data-id="${esc(c.id)}">Move to waiting</button>`}\n'
    '    </div>'
))

open(dst, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
