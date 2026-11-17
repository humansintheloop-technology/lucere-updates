"""Lucere v1.8.1: notes for the chat become "Ideas from <Chief>", each answered with a tap.
In Make it yours, each open note now has Yes, do it (Yes, fix it for a problem): it saves a wish from the note
and closes the note with its answer; No, leave it as is: closes it, with the answer "Don't suggest this again";
and Talk it through: copies it for the project chat. Both closes have Undo. setNote(id, status, answer) also
stores closedAt and answer on the note (new fields; nothing renamed), so the morning brief can read what was
answered and not suggest it again. The count by Make it yours reads "N ideas, N wishes to answer", and Today's
Make it yours card counts ideas too. Decisions about the day stay in Choices.
Run: python3 26_ideas_from_chief.py in.html out.html"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, 'expected one match (found %d) for: %s' % (n, old[:60])
    s = s.replace(old, new)


rep("function setNote(id, status){\n  if (wishStore()){ const n = (L.notes || []).find(x => x.id === id); if (n) n.status = status; dbWrite('notes/' + id, ref => ref.update({ status, closedAt:Date.now() })); }\n  else { const n = (S.chatNotes || []).find(x => x.id === id); if (n) n.status = status; save(); }\n",
    "function setNote(id, status, answer){\n  const patch = { status, closedAt:Date.now() }; if (answer) patch.answer = String(answer).slice(0, 200);\n  if (status === 'open'){ patch.answer = null; patch.closedAt = null; }\n  if (wishStore()){ const n = (L.notes || []).find(x => x.id === id); if (n) Object.assign(n, patch); dbWrite('notes/' + id, ref => ref.update(patch)); }\n  else { const n = (S.chatNotes || []).find(x => x.id === id); if (n) Object.assign(n, patch); save(); }\n")

rep("  if (N.length) parts.push(`${S.chief}'s notes for ${S.space}:\\n` + N.map((n, i) => `${i+1}. ${NOTE_KIND[n.kind] || 'Note'}: ${n.t}`).join('\\n'));\n  return parts.join('\\n\\n') || `Check ${S.chief}'s notes in ${S.space}.`;\n",
    "  if (N.length) parts.push(`Ideas from ${S.chief} for ${S.space}:\\n` + N.map((n, i) => `${i+1}. ${NOTE_KIND[n.kind] || 'Idea'}: ${n.t}`).join('\\n'));\n  return parts.join('\\n\\n') || `Check ${S.chief}'s ideas in ${S.space}.`;\n")

rep('      <button type="button" class="yours-btn" data-act="go" data-st="yours"${cur(\'yours\')}>${flower(\'\', .9, 2, journeyState().done)}<span><b>Make it yours</b><small>${reviewWishes().length ? `${reviewWishes().length} to keep or undo` : openWishes().length || openNotes().length ? [openWishes().length ? `${openWishes().length} ${openWishes().length === 1 ? \'wish\' : \'wishes\'}` : \'\', openNotes().length ? `${openNotes().length} ${openNotes().length === 1 ? \'note\' : \'notes\'}` : \'\'].filter(Boolean).join(\' \xb7 \') + \' waiting\' : \'Wish for anything\'}</small></span></button>\n',
    '      <button type="button" class="yours-btn" data-act="go" data-st="yours"${cur(\'yours\')}>${flower(\'\', .9, 2, journeyState().done)}<span><b>Make it yours</b><small>${reviewWishes().length ? `${reviewWishes().length} to keep or undo` : openWishes().length || openNotes().length ? [openWishes().length ? `${openWishes().length} ${openWishes().length === 1 ? \'wish\' : \'wishes\'}` : \'\', openNotes().length ? `${openNotes().length} ${openNotes().length === 1 ? \'idea\' : \'ideas\'}` : \'\'].filter(Boolean).join(\' \xb7 \') + \' to answer\' : \'Wish for anything\'}</small></span></button>\n')

rep('    <p class="small muted" style="margin:0">${S.nightly ? \'Wishes are built tonight while you sleep. In the morning, you keep or undo each one.\' : \'Your project chat builds each wish with you, and shows you first.\'} ${openWishes().length ? `${openWishes().length} ${openWishes().length === 1 ? \'wish\' : \'wishes\'} waiting. ` : \'\'}<button type="button" class="link small" data-act="go" data-st="yours">See how it grows</button></p>\n',
    '    <p class="small muted" style="margin:0">${S.nightly ? \'Wishes are built tonight while you sleep. In the morning, you keep or undo each one.\' : \'Your project chat builds each wish with you, and shows you first.\'} ${openWishes().length ? `${openWishes().length} ${openWishes().length === 1 ? \'wish\' : \'wishes\'} waiting. ` : \'\'}${openNotes().length ? `${openNotes().length} ${openNotes().length === 1 ? \'idea\' : \'ideas\'} from ${esc(S.chief)} to answer. ` : \'\'}<button type="button" class="link small" data-act="go" data-st="yours">See how it grows</button></p>\n')

rep('  <section class="ysec" id="y-notes" aria-labelledby="yn-h"><div class="sh"><h3 class="sec" id="yn-h">Notes for your chat</h3><span class="small muted">From ${esc(S.chief)}, the page, and your morning brief</span></div>\n',
    '  <section class="ysec" id="y-notes" aria-labelledby="yn-h"><div class="sh"><h3 class="sec" id="yn-h">Ideas from ${esc(S.chief)}</h3><span class="small muted">Changes to ${esc(S.space)} itself. Decisions about your day are in Choices.</span></div>\n')

rep('    ${openNotes().length ? openNotes().map(n => `<div class="notice"><p class="eyebrow">${esc(NOTE_KIND[n.kind] || \'Note\')} \xb7 ${esc(noteBy(n))} \xb7 ${esc(timeAgo(n.created) || \'\')}</p><p class="rule" style="font-size:20px">${esc(n.t)}</p><div class="row"><button type="button" class="link small" data-act="note-drop" data-id="${esc(n.id)}">Let it go</button></div></div>`).join(\'\') : `<p class="empty">No notes. When ${esc(S.chief)} can\u2019t do something or notices a way to improve, it shows up here.</p>`}\n    ${openNotes().length || openWishes().length ? `<div class="wiz-nav"><button type="button" class="btn soft" data-act="chat-copy">Copy wishes and notes for chat</button></div>` : \'\'}\n    <p class="small muted" style="margin-top:18px">Notes only suggest. Your ${esc(S.space)} chat reads them, and nothing changes until you say yes there.</p>\n',
    '    ${openNotes().length ? openNotes().map(n => `<div class="notice"><p class="eyebrow">${esc(NOTE_KIND[n.kind] || \'Note\')} \xb7 ${esc(noteBy(n))} \xb7 ${esc(timeAgo(n.created) || \'\')}</p><p class="rule" style="font-size:20px">${esc(n.t)}</p><div class="row note-acts"><button type="button" class="btn" data-act="note-yes" data-id="${esc(n.id)}">${n.kind === \'idea\' ? \'Yes, do it\' : \'Yes, fix it\'}</button><button type="button" class="btn ghost" data-act="note-no" data-id="${esc(n.id)}">No, leave it as is</button><button type="button" class="link small" data-act="note-talk" data-id="${esc(n.id)}">Talk it through</button></div></div>`).join(\'\') : `<p class="empty">No ideas waiting. When ${esc(S.chief)} can\u2019t do something or sees a way to make ${esc(S.space)} better, it shows up here for you to answer.</p>`}\n    ${openNotes().length || openWishes().length ? `<div class="wiz-nav"><button type="button" class="btn soft" data-act="chat-copy">Copy wishes and ideas for chat</button></div>` : \'\'}\n    <p class="small muted" style="margin-top:18px"><b>Yes</b> makes it a wish, built tonight or in your ${esc(S.space)} chat, and you keep or undo it after. <b>No</b> closes it, and ${esc(S.chief)} won\u2019t suggest it again. <b>Talk it through</b> copies it for your chat.</p>\n')

rep("  'note-drop': el => { const id = el.dataset.id; setNote(id, 'dismissed'); toast('Let go.', () => setNote(id, 'open')); },\n",
    "  'note-drop': el => { const id = el.dataset.id; setNote(id, 'dismissed'); toast('Let go.', () => setNote(id, 'open')); },\n  'note-yes': el => { const id = el.dataset.id, n = chatNotes().find(x => x.id === id); if (!n) return;\n    const w = newWish((n.kind === 'idea' ? '' : 'Fix: ') + n.t, 'you');\n    setNote(id, 'done', 'Yes, do it. Saved as a wish.');\n    toast(S.nightly ? 'Saved as a wish. It will be built tonight.' : 'Saved as a wish. Build it in your project chat.', () => { removeWish(w.id); setNote(id, 'open'); }); },\n  'note-no': el => { const id = el.dataset.id; setNote(id, 'dismissed', 'No, leave it as is. Don\u2019t suggest this again.'); toast('Left as is.', () => setNote(id, 'open')); },\n  'note-talk': el => { const n = chatNotes().find(x => x.id === el.dataset.id); if (n) copyText(`Let's talk about ${S.chief}'s idea for ${S.space}: ${n.t}`); },\n")

assert s.startswith('<!DOCTYPE html>')
open(dst, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
