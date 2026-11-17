"""Lucere v1.8.1: a part's keywords match whole words only.
"tea" (a cafe's keyword, say) no longer matches inside "teacher", so a parent-teacher conference stays with
Family. A plural s or es still counts ("tea" matches "teas"). Affects how mail and calendar events are sorted
into parts; no stored data changes. Run: python3 27_whole_word_keywords.py in.html out.html"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, 'expected one match (found %d) for: %s' % (n, old[:60])
    s = s.replace(old, new)


rep("function kwList(f){ const src = (S.keywords && S.keywords[f] != null) ? S.keywords[f] : KW_DEFAULT[f]; return String(src).split(',').map(x => x.trim().toLowerCase()).filter(Boolean); }\n",
    'function kwList(f){ const src = (S.keywords && S.keywords[f] != null) ? S.keywords[f] : KW_DEFAULT[f]; return String(src).split(\',\').map(x => x.trim().toLowerCase()).filter(Boolean); }\n/* whole words only (2026-11-16): "tea" no longer matches inside "teacher"; a plural s or es still counts */\nconst KW_RE = {};\nfunction kwHit(t, k){ const re = KW_RE[k] || (KW_RE[k] = new RegExp(\'(^|[^a-z0-9])\' + k.replace(/[.*+?^${}()|[\\]\\\\]/g, \'\\\\$&\') + \'(e?s)?(?=$|[^a-z0-9])\')); return re.test(t); }\n')

rep("  for (const f of ['work2','sc','work','family','home']) if (kwList(f).some(k => t.includes(k))) return f;\n",
    "  for (const f of ['work2','sc','work','family','home']) if (kwList(f).some(k => kwHit(t, k))) return f;\n")

assert s.startswith('<!DOCTYPE html>')
open(dst, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
