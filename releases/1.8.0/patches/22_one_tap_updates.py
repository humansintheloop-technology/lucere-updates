"""Lucere v1.8.0 (beta): updates install with a tap on Today, and undo with a tap on Trust.
The nightly (or morning) run prepares an update on a copy of the page, checks every file, tests it, and saves
the new page beside this one under updates/. Nothing changes until the owner taps Update, then Yes; then the
page publishes that prepared copy of itself. Before it does, the page checks: the copy matches its fingerprint
and version, the page hasn't changed since the copy was made, the owner's own settings block is unchanged, and
the copy adds no way to send or share. Undo publishes the copy from before the same way. Updates that carry a
skill, a doc, instructions, or a new capability still go through the project chat.
Raises the page's version to 1.8.0. Run: python3 22_one_tap_updates.py in.html out.html"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, 'expected one match (found %d) for: %s' % (n, old[:60])
    s = s.replace(old, new)


rep("const KIT_VERSION = '1.7.5';",
    "const KIT_VERSION = '1.8.0';")

rep(".upd-card .small{margin:0}\n",
    ".upd-card .small{margin:0}\n"
    ".upd-card .upd-acts{display:flex; gap:10px; flex-wrap:wrap; align-items:center}\n"
    ".upd-ask{flex:1 1 100%; margin:4px 0 0; padding:14px 16px; border-radius:var(--r-md, 14px); background:var(--surface); border:1px solid var(--line)}\n"
    ".upd-ask ul{margin:6px 0 10px; padding-left:18px}\n"
    ".upd-ask li{margin:2px 0}\n"
    ".upd-err{color:var(--warn-ink, var(--ink)); margin:6px 0 0}\n")

rep("function updReady(){ return !!(live() && L.update && L.update.latest && verGt(L.update.latest, S.kit_version || KIT_VERSION)); }\n",
    "function updReady(){ return !!(live() && L.update && L.update.latest && verGt(L.update.latest, S.kit_version || KIT_VERSION)); }\n"
    "/* ---------- one-tap updates (Lucere v1.8.0) ----------\n"
    "   The nightly or morning run prepares an update on a copy of this page, checks every file against its fingerprint,\n"
    "   tests it, and saves the new page beside this one, under updates/. Nothing changes until you tap Update, then Yes;\n"
    "   then this page publishes the prepared copy of itself. Undo publishes the copy from before. The page refuses a copy\n"
    "   that doesn't match, that would change your own settings, or that adds a way to send or share. */\n"
    "let ART = null;\n"
    "const UPD = { step:'', busy:false, err:'', fin:false };\n"
    "const UPD_FILE = /^updates\\/[A-Za-z0-9._-]+\\.html$/, UPD_SHA = /^[0-9a-f]{64}$/;\n"
    "async function updSha(t){ const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join(''); }\n"
    "async function updGet(p){ const r = await fetch(p, { cache:'no-store' }); if (!r.ok) throw { u:'missing' }; const t = await r.text(); return { t, sha:await updSha(t) }; }\n"
    "function updPerson(t){ const m = String(t).match(/<script type=\"application\\/json\" id=\"os-person\">([\\s\\S]*?)<\\/script>/); return m ? m[1].trim() : null; }\n"
    "function updRisk(t){ return (String(t).match(/['\"](?:reply|send|send_message|send_email|forward|forward_thread|forward_message|trash_thread|trash_message|delete_event|delete_draft|delete_label|respond_to_event|share_file|update_event)['\"]/g) || []).length; }\n"
    "function updOne(){ const u = L.update, r = u && u.ready; return !!(updReady() && ART && L.canWrite && r && r.to === u.latest && r.from === KIT_VERSION && r.tested === 'pass' && UPD_FILE.test(r.file || '') && UPD_FILE.test(r.before || '') && UPD_SHA.test(r.sha256 || '') && UPD_SHA.test(r.beforeSha || '') && !(r.chat && r.chat.length)); }\n"
    "function updCanUndo(){ const n = L.update && L.update.undo; return !!(live() && ART && L.canWrite && n && n.from === KIT_VERSION && n.to && UPD_FILE.test(n.file || '') && UPD_SHA.test(n.sha256 || '')); }\n"
    "function updMsg(c){ return ({ changed:'Your space changed after this update was prepared, so nothing changed. It will be prepared again tonight.', person:'This update would change your own settings, so nothing changed. Say \\u201cReport a problem\\u201d in your project chat.', risk:'This update touches sending or sharing, so it needs your yes in your project chat. Say \\u201cupdate Lucere\\u201d there.', conflict:'Your page changed a moment ago, so nothing was updated. Try again.', rate_limited:'That was a lot at once. Try again in a minute.', undochanged:'Your page changed after this update, so Undo here would also take that out. Say \\u201cgo back\\u201d in your project chat instead.' })[c] || 'That didn\\u2019t go through, and nothing changed. Try again, or say \\u201cupdate Lucere\\u201d in your project chat.'; }\n"
    "async function updApply(kind){\n"
    "  if (UPD.busy) return;\n"
    "  const u = L.update || {}, r = kind === 'undo' ? u.undo : u.ready;\n"
    "  if (!r || !(kind === 'undo' ? updCanUndo() : updOne())) return;\n"
    "  UPD.busy = true; UPD.err = ''; render();\n"
    "  let wrote = false;\n"
    "  try {\n"
    "    const cur = await updGet('index.html');\n"
    "    if (kind === 'update' && cur.sha !== r.beforeSha) throw { u:'changed' };\n"
    "    if (kind === 'undo' && r.afterSha && cur.sha !== r.afterSha) throw { u:'undochanged' };\n"
    "    const next = await updGet(r.file);\n"
    "    if (next.sha !== r.sha256 || !/^<!DOCTYPE html>/i.test(next.t)) throw { u:'match' };\n"
    "    const m = next.t.match(/const KIT_VERSION = '([0-9.]+)'/);\n"
    "    if (!m || m[1] !== r.to) throw { u:'match' };\n"
    "    if (updPerson(next.t) !== updPerson(cur.t)) throw { u:'person' };\n"
    "    if (kind === 'update' && updRisk(next.t) > updRisk(cur.t)) throw { u:'risk' };\n"
    "    const applying = { kind, to:r.to, from:KIT_VERSION, at:Date.now(), title:kind === 'undo' ? '' : String(u.title || ''), undo:kind === 'update' ? { file:r.before, sha256:r.beforeSha } : null };\n"
    "    await dbWrite('update/main', ref => ref.set(Object.assign({}, u, { applying })));\n"
    "    wrote = true;\n"
    "    UPD.step = 'going'; render();\n"
    "    await ART.publish(next.t);\n"
    "  } catch(e) {\n"
    "    const c = (e && (e.u || e.code)) || '';\n"
    "    if (wrote){ const back = Object.assign({}, L.update || u); delete back.applying; dbWrite('update/main', ref => ref.set(back)); }\n"
    "    UPD.busy = false; UPD.step = ''; UPD.err = (c === 'not_writer' || c === 'not_granted') ? 'Updating from this view isn\\u2019t available. Say \\u201cupdate Lucere\\u201d in your project chat.' : updMsg(c);\n"
    "    render();\n"
    "  }\n"
    "}\n"
    "async function updFinish(){\n"
    "  const u = L.update, a = u && u.applying;\n"
    "  if (!a || UPD.fin || !L.canWrite || !live()) return;\n"
    "  UPD.fin = true;\n"
    "  if (KIT_VERSION === a.to){\n"
    "    let me = null; try { me = await updGet('index.html'); } catch(e) {}\n"
    "    const next = Object.assign({}, u); delete next.applying; delete next.ready; delete next.undo;\n"
    "    next.latest = verGt(u.latest || '0', a.to) ? u.latest : a.to;\n"
    "    if (a.kind === 'update' && a.undo) next.undo = { to:a.from, from:a.to, file:a.undo.file, sha256:a.undo.sha256, afterSha:me ? me.sha : null };\n"
    "    await dbWrite('update/main', ref => ref.set(next));\n"
    "    if (a.kind === 'undo') addLog(`Went back to Lucere v${a.to}.`, { kind:'update', cls:'B', by:'you', detail:'On your tap. Every file checked.' });\n"
    "    else addLog(`Updated to Lucere v${a.to}${a.title ? ': ' + a.title : ''}.`, { kind:'update', cls:'B', by:'you', detail:`On your tap. Every file checked and tested first. To undo, tap Undo on the Trust page, or say \\u201cgo back to v${a.from}\\u201d in your project chat.` });\n"
    "    toast(a.kind === 'undo' ? `You\\u2019re back on Lucere v${a.to}.` : `You\\u2019re on Lucere v${a.to}. Undo is on the Trust page.`);\n"
    "  } else if (Date.now() - (a.at || 0) > 120000){\n"
    "    const next = Object.assign({}, u); delete next.applying;\n"
    "    await dbWrite('update/main', ref => ref.set(next));\n"
    "    toast('The update didn\\u2019t finish, so nothing changed.');\n"
    "  } else UPD.fin = false;\n"
    "}\n"
    "function updBox(where){\n"
    "  const u = L.update || {}, r = u.ready || {}, one = updOne();\n"
    "  if (UPD.step === 'going') return `<p class=\"small muted\">Updating now. Your page will reload in a moment.</p>`;\n"
    "  if (UPD.step === 'ask' && one){\n"
    "    const notes = Array.isArray(r.notes) && r.notes.length ? r.notes : [{ version:u.latest, title:u.title || '', note:u.note || '' }];\n"
    "    return `<div class=\"upd-ask\"><p style=\"margin:0\"><b>What\\u2019s new</b></p><ul>${notes.map(n => `<li><b>${esc(n.title || 'v' + n.version)}</b>${n.note ? ' \\u00b7 ' + esc(n.note) : ''}</li>`).join('')}</ul><p class=\"small muted\" style=\"margin:0 0 10px\">It was checked and tested on a copy of your space first. Your names, wishes, helpers and data stay as they are. You can undo it anytime on the Trust page.</p><div class=\"upd-acts\"><button type=\"button\" class=\"btn\" data-act=\"upd-yes\"${UPD.busy ? ' disabled' : ''}>Yes, update</button><button type=\"button\" class=\"btn ghost\" data-act=\"upd-cancel\">Not now</button></div></div>`;\n"
    "  }\n"
    "  const err = UPD.err ? `<p class=\"small upd-err\">${esc(UPD.err)}</p>` : '';\n"
    "  if (one) return `<p class=\"small muted\">Ready to install. Tap Update to see what\\u2019s new. Nothing changes until you say yes.</p>${err}<div class=\"upd-acts\" style=\"margin-top:8px\"><button type=\"button\" class=\"btn\" data-act=\"upd-open\">Update</button>${where === 'today' ? '<button type=\"button\" class=\"btn ghost\" data-act=\"go\" data-st=\"trust\">See it on Trust</button>' : ''}</div>`;\n"
    "  if (r.chat && r.chat.length) return `<p class=\"small muted\">This one includes a part to save in your project chat. When you have five minutes, say &ldquo;update Lucere&rdquo; there. Nothing changes until you say yes.</p>${err}`;\n"
    "  return `<p class=\"small muted\">When you have five minutes, say &ldquo;update Lucere&rdquo; in your project chat. You&rsquo;ll see what&rsquo;s new first, and nothing changes until you say yes.</p>${err}`;\n"
    "}\n")

rep("  return `<section class=\"upd-card${u.essential ? ' essential' : ''}\" id=\"t-update\" aria-labelledby=\"upd-h\">${gem()}<div class=\"upd-body\"><p class=\"eyebrow\" id=\"upd-h\">${u.essential ? 'Important update ready' : 'New in Lucere'} &middot; v${esc(u.latest)}</p><p class=\"upd-t\">${esc(u.title || 'A new version of Lucere is ready.')}</p><p class=\"small muted\">When you have five minutes, say &ldquo;update Lucere&rdquo; in your project chat. You&rsquo;ll see what&rsquo;s new first, and nothing changes until you say yes.</p></div><button type=\"button\" class=\"btn ghost\" data-act=\"go\" data-st=\"trust\">See it on Trust</button></section>`;",
    "  const one = updOne() || UPD.step === 'going';\n"
    "  return `<section class=\"upd-card${u.essential ? ' essential' : ''}\" id=\"t-update\" aria-labelledby=\"upd-h\">${gem()}<div class=\"upd-body\"><p class=\"eyebrow\" id=\"upd-h\">${u.essential ? 'Important update ready' : 'New in Lucere'} &middot; v${esc(u.latest)}</p><p class=\"upd-t\">${esc(u.title || 'A new version of Lucere is ready.')}</p>${updBox('today')}</div>${one ? '' : '<button type=\"button\" class=\"btn ghost\" data-act=\"go\" data-st=\"trust\">See it on Trust</button>'}</section>`;")

rep("    ${updReady() ? `<div class=\"panel\" style=\"margin-top:14px\"><p class=\"eyebrow\">${L.update.essential ? 'Important update ready' : 'Update ready'} \u00b7 v${esc(L.update.latest)}</p><p style=\"margin-top:8px\">${esc(L.update.title || 'A new version of Lucere.')}</p><p class=\"small muted\" style=\"margin-top:8px\">When you have five minutes, say \u201cupdate Lucere\u201d in your project chat. You\u2019ll see what\u2019s new first, and nothing changes until you say yes.</p></div>` : ''}\n"
    "    <p class=\"small muted\" style=\"margin-top:12px\">Every update is written down below. To undo one, say \u201cgo back to v${esc(S.kit_version || KIT_VERSION)}\u201d before the next, or name any earlier version, in your project chat.</p></section>",
    "    ${updReady() ? `<div class=\"panel\" style=\"margin-top:14px\"><p class=\"eyebrow\">${L.update.essential ? 'Important update ready' : 'Update ready'} \u00b7 v${esc(L.update.latest)}</p><p style=\"margin-top:8px\">${esc(L.update.title || 'A new version of Lucere.')}</p><div style=\"margin-top:8px\">${updBox('trust')}</div></div>` : ''}\n"
    "    ${updCanUndo() ? `<div class=\"panel\" style=\"margin-top:14px\"><p class=\"eyebrow\">Undo the last update</p><p class=\"small muted\" style=\"margin-top:8px\">Puts your page back as it was on v${esc(L.update.undo.to)}. Nothing else changes.</p>${UPD.step === 'undo-ask' ? `<div class=\"upd-acts\" style=\"margin-top:8px\"><button type=\"button\" class=\"btn\" data-act=\"upd-undo-yes\"${UPD.busy ? ' disabled' : ''}>Yes, go back to v${esc(L.update.undo.to)}</button><button type=\"button\" class=\"btn ghost\" data-act=\"upd-cancel\">Keep it</button></div>` : `<div class=\"upd-acts\" style=\"margin-top:8px\"><button type=\"button\" class=\"btn ghost\" data-act=\"upd-undo\">Undo update</button></div>`}${UPD.err && !updReady() ? `<p class=\"small upd-err\">${esc(UPD.err)}</p>` : ''}</div>` : ''}\n"
    "    <p class=\"small muted\" style=\"margin-top:12px\">Every update is written down below. To undo one, tap Undo update here, or say \u201cgo back to v${esc(S.kit_version || KIT_VERSION)}\u201d before the next, or name any earlier version, in your project chat.</p></section>")

rep("  L.unsub.push(db.doc('update/main').onSnapshot(s => { L.update = s.exists ? s.data() : null; renderSoon(); }, dbErr));",
    "  L.unsub.push(db.doc('update/main').onSnapshot(s => { L.update = s.exists ? s.data() : null; renderSoon(); if (!(s.metadata && s.metadata.fromCache)) updFinish(); }, dbErr));")

rep("  L.mcp = mcp; L.db = db; L.user = user;\n",
    "  L.mcp = mcp; L.db = db; L.user = user;\n"
    "  use('artifact').then(a => { ART = a || null; renderSoon(); });\n")

rep("  'go': el => go(el.dataset.st),\n",
    "  'go': el => go(el.dataset.st),\n"
    "  'upd-open': () => { UPD.step = 'ask'; UPD.err = ''; render(); },\n"
    "  'upd-cancel': () => { if (!UPD.busy){ UPD.step = ''; UPD.err = ''; render(); } },\n"
    "  'upd-yes': () => updApply('update'),\n"
    "  'upd-undo': () => { UPD.step = 'undo-ask'; UPD.err = ''; render(); },\n"
    "  'upd-undo-yes': () => updApply('undo'),\n")

assert s.startswith('<!DOCTYPE html>')
open(dst, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
