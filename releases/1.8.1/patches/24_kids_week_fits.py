"""Lucere v1.8.1: the kids' week reads well at any width.
The week follows its own card's width, not the screen's (on iPad with the side menu showing, the old rule left
seven squashed columns with words broken mid-word). Under 860px of its own width it becomes a list of days: the
day on the left, plans on the right, "Nothing planned" on free days. Words wrap whole. Looks only.
Raises the page's version to 1.8.1. Run: python3 24_kids_week_fits.py in.html out.html"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, 'expected one match (found %d) for: %s' % (n, old[:60])
    s = s.replace(old, new)


rep("const KIT_VERSION = '1.8.0';",
    "const KIT_VERSION = '1.8.1';")

rep('.ad li{overflow-wrap:anywhere}',
    '.ad li{overflow-wrap:break-word; hyphens:auto}')

rep('@media (max-width:1100px){ .aweek{grid-template-columns:minmax(0,1fr); gap:6px} .ad{display:grid; grid-template-columns:76px minmax(0,1fr); gap:12px; align-items:baseline; padding:10px 14px} .adl{margin:0} .ad ul{gap:4px} .ad .at{display:inline; margin-right:6px} }\n',
    '@media (max-width:1100px){ .aweek{grid-template-columns:minmax(0,1fr); gap:6px} .ad{display:grid; grid-template-columns:76px minmax(0,1fr); gap:12px; align-items:baseline; padding:10px 14px} .adl{margin:0} .ad ul{gap:4px} .ad .at{display:inline; margin-right:6px} }\n/* The kids\' week follows its own width, not the screen\'s (v1.8.1): under 860px it is a list of days */\n#t-kidsweek{container-type:inline-size; container-name:kweek}\n@container kweek (max-width: 860px){\n  .aweek{grid-template-columns:minmax(0,1fr); gap:6px}\n  .ad{display:grid; grid-template-columns:84px minmax(0,1fr); gap:14px; align-items:baseline; padding:12px 16px; border-radius:18px 22px 18px 22px}\n  .adl{margin:0; white-space:nowrap}\n  .ad ul{gap:6px; font-size:15px; line-height:1.4}\n  .ad .at{display:inline; margin-right:8px; font-size:12.5px}\n  .ade{margin:0; font-size:0; color:var(--muted)}\n  .ade::after{content:"Nothing planned"; font-size:14px; opacity:.75}\n}\n')

assert s.startswith('<!DOCTYPE html>')
open(dst, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
