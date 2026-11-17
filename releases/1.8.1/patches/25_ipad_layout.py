"""Lucere v1.8.1: iPad looks even, nothing slides sideways, and small labels are easier to read.
- Today and Make it yours are one even column below a 1440px screen (two columns only when there's real room
  beside the side menu). Phones are unchanged; big screens keep two columns.
- No side-to-side scrolling: html and body clip sideways overflow (overflow-x:clip keeps the side menu and the
  top bar sticky), the Chief's closed panel takes no taps, and the shaped cards keep their soft blob inside.
- iPad upright (641 to 860px): every tab shows on two rows instead of a sideways swipe row; phones keep the swipe.
- The Chief's suggestion chips wrap from 641px up.
- Small uppercase labels go from 10.5px to 11.5px below 1440px.
Looks only. Run: python3 25_ipad_layout.py in.html out.html"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, 'expected one match (found %d) for: %s' % (n, old[:60])
    s = s.replace(old, new)


rep('@media (max-width:1100px){ .grid2{grid-template-columns:minmax(0,1fr)} }\n',
    "@media (max-width:1100px){ .grid2{grid-template-columns:minmax(0,1fr)} }\n/* iPad (v1.8.1): with the side menu showing, two columns only once there's real room for them; until then one even column */\n@media (max-width:1439px){ .grid2{grid-template-columns:minmax(0,1fr); row-gap:28px} .grid2 > .stack{min-width:0} #t-yours{max-width:none !important} }\n/* No side-to-side scrolling on iPad or phone (v1.8.1): Safari can pan to the Chief's closed panel, which waits off-screen. Clip sideways overflow at the root; clip (not hidden) keeps the side menu and top bar sticky. */\n@supports (overflow:clip){ html, body{overflow-x:clip} }\nhtml, body{overscroll-behavior-x:none}\n.chief:not(.open){pointer-events:none}\n/* Cards keep their soft shapes inside their own edges, so nothing pokes past the screen. */\n.bloom{contain:paint}\n/* iPad upright: every tab shows at once, on two rows, with no sideways scroll. Phones keep the swipeable row. */\n@media (min-width:641px) and (max-width:860px){\n  .strip{flex-wrap:wrap; overflow-x:visible; margin-right:0; padding-right:0; row-gap:8px}\n}\n/* In the Chief's panel on iPad, suggestions sit on two rows instead of sliding sideways. */\n@media (min-width:641px){ .quick{flex-wrap:wrap; overflow-x:visible; row-gap:8px} }\n@supports (overflow:clip){ .bloom{overflow:clip} }\n")

rep('</style>',
    "/* Small labels a touch larger on iPad and phone (v1.8.1), so they're easy to read at arm's length. */\n@media (max-width:1439px){\n  .tag, .brand-sub, .nn .lbl, .pill, .choice .said span, .chief-head .rl, .chief-sub .eyebrow, .dec-top, .dec-gh{font-size:11.5px}\n  .opt .reclbl{font-size:11px} .dec .pri{font-size:10.5px}\n}\n</style>")

assert s.startswith('<!DOCTYPE html>')
open(dst, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
