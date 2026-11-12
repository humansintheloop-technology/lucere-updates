"""Lucere v1.7.2 (beta): when a new version is ready, a card at the top of Today says so,
with what it brings and what to say. It shows only while an update is waiting.
Raises the page's version to 1.7.2. Run: python3 18_update_on_today.py in.html out.html"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, 'expected one match (found %d) for: %s' % (n, old[:60])
    s = s.replace(old, new)


rep("const KIT_VERSION = '1.7.1';", "const KIT_VERSION = '1.7.2';")

rep(".night-card .row{margin-top:12px}\n",
    ".night-card .row{margin-top:12px}\n"
    ".upd-card{display:flex; gap:18px; align-items:center; flex-wrap:wrap; padding:18px 24px; margin:0 0 22px;"
    " border-radius:var(--r-lg); border:1px solid var(--line); background:linear-gradient(120deg, var(--accent-soft), var(--surface));"
    " box-shadow:var(--shadow)}\n"
    ".upd-card.essential{border-color:var(--warn); background:linear-gradient(120deg, var(--warn-soft), var(--surface))}\n"
    ".upd-card .gem{width:40px; height:40px; flex:none}\n"
    ".upd-card .upd-body{flex:1 1 280px; min-width:0}\n"
    ".upd-card .eyebrow{margin:0}\n"
    ".upd-card .upd-t{margin:4px 0 2px; font-family:var(--f-display); font-size:clamp(20px, 2.2vw, 26px); line-height:1.15}\n"
    ".upd-card .small{margin:0}\n")

rep("function liveBanner(){",
    "function updateCard(){\n"
    "  if (!updReady()) return '';\n"
    "  const u = L.update;\n"
    "  return `<section class=\"upd-card${u.essential ? ' essential' : ''}\" id=\"t-update\" aria-labelledby=\"upd-h\">${gem()}"
    "<div class=\"upd-body\"><p class=\"eyebrow\" id=\"upd-h\">${u.essential ? 'Important update ready' : 'New in Lucere'} &middot; v${esc(u.latest)}</p>"
    "<p class=\"upd-t\">${esc(u.title || 'A new version of Lucere is ready.')}</p>"
    "<p class=\"small muted\">When you have five minutes, say &ldquo;update Lucere&rdquo; in your project chat. "
    "You&rsquo;ll see what&rsquo;s new first, and nothing changes until you say yes.</p></div>"
    "<button type=\"button\" class=\"btn ghost\" data-act=\"go\" data-st=\"trust\">See it on Trust</button></section>`;\n"
    "}\n"
    "function liveBanner(){")

rep("  ${liveBanner()}\n  <section class=\"hero\" id=\"t-hero\">",
    "  ${liveBanner()}\n  ${updateCard()}\n  <section class=\"hero\" id=\"t-hero\">")

open(dst, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
