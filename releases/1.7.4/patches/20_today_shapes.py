"""Lucere v1.7.4 (beta): Today's sections become soft, shaped cards.
The day, the kids' week, Making room for, Choices waiting, Due today, Steep, and A thought for today
each get their own gentle gradient, rounded uneven corners, a soft glow, and a curved line at the bottom,
in light and dark. Looks only: no data, wording, or behavior changes.
Raises the page's version to 1.7.4. Run: python3 20_today_shapes.py in.html out.html"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, 'expected one match (found %d) for: %s' % (n, old[:60])
    s = s.replace(old, new)


rep("const KIT_VERSION = '1.7.3';",
    "const KIT_VERSION = '1.7.4';")

rep((
    '</style>\n'
    '\n'
    '<div class="opal" aria-hidden="true"></div>'
),
    (
    "/* ---------- Today's sections as soft shaped cards (Lucere v1.7.4) ---------- */\n"
    '.stack:has(> .bloom){gap:28px}\n'
    '.bloom{position:relative; isolation:isolate; overflow:hidden; padding:30px 30px 46px;\n'
    '  border-radius:46px 22px 52px 26px / 34px 46px 28px 52px;\n'
    '  background:linear-gradient(140deg, var(--bl-a), var(--bl-b) 58%, var(--bl-c));\n'
    '  box-shadow:0 1px 2px hsl(var(--h) 30% 25% / .04), 0 24px 46px -28px var(--bl-sh)}\n'
    '.bloom::before{content:""; position:absolute; z-index:-1; right:-70px; top:-80px; width:240px; height:240px; pointer-events:none;\n'
    '  border-radius:58% 42% 63% 37% / 45% 55% 45% 55%; background:radial-gradient(circle at 38% 38%, var(--bl-blob), transparent 70%)}\n'
    '.bloom::after{content:""; position:absolute; z-index:-1; left:0; right:0; bottom:0; height:50px; pointer-events:none; opacity:.45;\n'
    '  background:var(--bl-line); -webkit-mask:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 400 70\' preserveAspectRatio=\'none\'%3E%3Cpath d=\'M0 40 C 70 6, 140 66, 210 36 S 335 8, 400 30\' fill=\'none\' stroke=\'black\' stroke-width=\'1.3\' vector-effect=\'non-scaling-stroke\'/%3E%3Cpath d=\'M0 54 C 90 26, 160 74, 230 50 S 345 28, 400 46\' fill=\'none\' stroke=\'black\' stroke-width=\'.9\' vector-effect=\'non-scaling-stroke\'/%3E%3C/svg%3E") no-repeat bottom / 100% 100%; mask:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 400 70\' preserveAspectRatio=\'none\'%3E%3Cpath d=\'M0 40 C 70 6, 140 66, 210 36 S 335 8, 400 30\' fill=\'none\' stroke=\'black\' stroke-width=\'1.3\' vector-effect=\'non-scaling-stroke\'/%3E%3Cpath d=\'M0 54 C 90 26, 160 74, 230 50 S 345 28, 400 46\' fill=\'none\' stroke=\'black\' stroke-width=\'.9\' vector-effect=\'non-scaling-stroke\'/%3E%3C/svg%3E") no-repeat bottom / 100% 100%}\n'
    '.bloom .sec{font-size:29px}\n'
    '.bloom .empty{background:hsl(0 0% 100% / .45); border-radius:18px 26px 18px 26px; padding:12px 16px}\n'
    '.b-day{--bl-a:hsl(345 80% 96.5%); --bl-b:hsl(18 85% 95.5%); --bl-c:hsl(36 90% 96.5%); --bl-blob:hsl(340 85% 88% / .6); --bl-line:hsl(345 52% 62%); --bl-sh:hsl(345 50% 40% / .28)}\n'
    '.b-kids{border-radius:24px 54px 28px 48px / 50px 28px 46px 30px;\n'
    '  --bl-a:hsl(28 90% 95.5%); --bl-b:hsl(356 80% 95.5%); --bl-c:hsl(322 60% 96.5%); --bl-blob:hsl(20 90% 86% / .55); --bl-line:hsl(16 60% 58%); --bl-sh:hsl(16 50% 40% / .26)}\n'
    '.b-choices{border-radius:52px 26px 40px 24px / 30px 52px 34px 48px;\n'
    '  --bl-a:hsl(276 62% 96.5%); --bl-b:hsl(320 60% 96%); --bl-c:hsl(346 70% 97%); --bl-blob:hsl(282 60% 86% / .55); --bl-line:hsl(284 36% 60%); --bl-sh:hsl(284 40% 40% / .28)}\n'
    '.b-due{border-radius:28px 50px 24px 44px / 46px 26px 52px 30px;\n'
    '  --bl-a:hsl(150 36% 95%); --bl-b:hsl(62 52% 95.5%); --bl-c:hsl(40 72% 96.5%); --bl-blob:hsl(150 42% 83% / .55); --bl-line:hsl(150 28% 48%); --bl-sh:hsl(150 30% 30% / .24)}\n'
    '.b-steep{border-radius:44px 24px 50px 30px / 28px 50px 30px 46px;\n'
    '  --bl-a:hsl(205 62% 96%); --bl-b:hsl(250 55% 96.5%); --bl-c:hsl(302 50% 97%); --bl-blob:hsl(210 62% 86% / .55); --bl-line:hsl(222 38% 60%); --bl-sh:hsl(222 40% 40% / .26)}\n'
    '.b-thought{border-radius:30px 48px 26px 54px / 48px 30px 50px 26px;\n'
    '  --bl-a:hsl(42 86% 95%); --bl-b:hsl(18 82% 95.5%); --bl-c:hsl(346 70% 97%); --bl-blob:hsl(40 86% 83% / .55); --bl-line:hsl(30 56% 52%); --bl-sh:hsl(30 50% 35% / .24)}\n'
    '.b-room{border-radius:50px 24px 46px 28px / 32px 48px 30px 50px;\n'
    '  --bl-a:hsl(330 70% 96.5%); --bl-b:hsl(290 50% 96.5%); --bl-c:hsl(250 55% 97%); --bl-blob:hsl(320 70% 87% / .55); --bl-line:hsl(318 40% 62%); --bl-sh:hsl(318 40% 40% / .26)}\n'
    '.bloom.why-card{border:0}\n'
    ':root[data-theme="dark"] .b-room{--bl-a:hsl(330 24% 14%); --bl-b:hsl(290 20% 14%); --bl-c:hsl(250 22% 13.5%); --bl-blob:hsl(320 34% 30% / .5); --bl-line:hsl(318 44% 74%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    '@media (prefers-color-scheme: dark){\n'
    '  :root:not([data-theme="light"]) .b-room{--bl-a:hsl(330 24% 14%); --bl-b:hsl(290 20% 14%); --bl-c:hsl(250 22% 13.5%); --bl-blob:hsl(320 34% 30% / .5); --bl-line:hsl(318 44% 74%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    '  :root:not([data-theme="light"]) .bloom .empty{background:hsl(0 0% 100% / .05)}\n'
    '  :root:not([data-theme="light"]) .b-day{--bl-a:hsl(345 26% 14%); --bl-b:hsl(18 24% 13%); --bl-c:hsl(36 22% 12.5%); --bl-blob:hsl(340 40% 30% / .5); --bl-line:hsl(345 50% 70%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    '  :root:not([data-theme="light"]) .b-kids{--bl-a:hsl(28 26% 13.5%); --bl-b:hsl(356 24% 13.5%); --bl-c:hsl(322 20% 13%); --bl-blob:hsl(20 40% 30% / .5); --bl-line:hsl(16 56% 68%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    '  :root:not([data-theme="light"]) .b-choices{--bl-a:hsl(276 24% 14%); --bl-b:hsl(320 22% 13.5%); --bl-c:hsl(346 22% 13%); --bl-blob:hsl(282 34% 32% / .5); --bl-line:hsl(284 40% 74%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    '  :root:not([data-theme="light"]) .b-due{--bl-a:hsl(150 18% 12.5%); --bl-b:hsl(62 16% 12.5%); --bl-c:hsl(40 20% 12.5%); --bl-blob:hsl(150 26% 28% / .5); --bl-line:hsl(150 30% 62%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    '  :root:not([data-theme="light"]) .b-steep{--bl-a:hsl(205 26% 13.5%); --bl-b:hsl(250 22% 14%); --bl-c:hsl(302 18% 13%); --bl-blob:hsl(210 34% 30% / .5); --bl-line:hsl(222 44% 74%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    '  :root:not([data-theme="light"]) .b-thought{--bl-a:hsl(42 26% 12.5%); --bl-b:hsl(18 24% 13%); --bl-c:hsl(346 20% 13%); --bl-blob:hsl(40 40% 28% / .5); --bl-line:hsl(36 58% 66%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    '}\n'
    ':root[data-theme="dark"] .bloom .empty{background:hsl(0 0% 100% / .05)}\n'
    ':root[data-theme="dark"] .b-day{--bl-a:hsl(345 26% 14%); --bl-b:hsl(18 24% 13%); --bl-c:hsl(36 22% 12.5%); --bl-blob:hsl(340 40% 30% / .5); --bl-line:hsl(345 50% 70%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    ':root[data-theme="dark"] .b-kids{--bl-a:hsl(28 26% 13.5%); --bl-b:hsl(356 24% 13.5%); --bl-c:hsl(322 20% 13%); --bl-blob:hsl(20 40% 30% / .5); --bl-line:hsl(16 56% 68%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    ':root[data-theme="dark"] .b-choices{--bl-a:hsl(276 24% 14%); --bl-b:hsl(320 22% 13.5%); --bl-c:hsl(346 22% 13%); --bl-blob:hsl(282 34% 32% / .5); --bl-line:hsl(284 40% 74%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    ':root[data-theme="dark"] .b-due{--bl-a:hsl(150 18% 12.5%); --bl-b:hsl(62 16% 12.5%); --bl-c:hsl(40 20% 12.5%); --bl-blob:hsl(150 26% 28% / .5); --bl-line:hsl(150 30% 62%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    ':root[data-theme="dark"] .b-steep{--bl-a:hsl(205 26% 13.5%); --bl-b:hsl(250 22% 14%); --bl-c:hsl(302 18% 13%); --bl-blob:hsl(210 34% 30% / .5); --bl-line:hsl(222 44% 74%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    ':root[data-theme="dark"] .b-thought{--bl-a:hsl(42 26% 12.5%); --bl-b:hsl(18 24% 13%); --bl-c:hsl(346 20% 13%); --bl-blob:hsl(40 40% 28% / .5); --bl-line:hsl(36 58% 66%); --bl-sh:hsl(0 0% 0% / .5)}\n'
    '@media (max-width:640px){ .bloom{padding:24px 20px 42px} .bloom .sec{font-size:26px} }\n'
    '</style>\n'
    '\n'
    '<div class="opal" aria-hidden="true"></div>'
))

rep('  if (!R.length) return `<section class="why-card" id="t-why" aria-labelledby="why-h">',
    '  if (!R.length) return `<section class="why-card bloom b-room" id="t-why" aria-labelledby="why-h">')

rep('  return `<section class="why-card" id="t-why" aria-labelledby="why-h">',
    '  return `<section class="why-card bloom b-room" id="t-why" aria-labelledby="why-h">')

rep('      <section id="t-day" aria-labelledby="day-h">',
    '      <section class="bloom b-day" id="t-day" aria-labelledby="day-h">')

rep('      <section id="t-choices" aria-labelledby="ch-h">',
    '      <section class="bloom b-choices" id="t-choices" aria-labelledby="ch-h">')

rep('      <section aria-labelledby="rem-h">',
    '      <section class="bloom b-due" aria-labelledby="rem-h">')

rep('      <section id="t-steep" aria-labelledby="steep-h">',
    '      <section class="bloom b-steep" id="t-steep" aria-labelledby="steep-h">')

rep('      <section aria-label="A thought for today">',
    '      <section class="bloom b-thought" aria-label="A thought for today">')

rep('  return `<section id="t-kidsweek" aria-labelledby="kw-h">',
    '  return `<section class="bloom b-kids" id="t-kidsweek" aria-labelledby="kw-h">')

open(dst, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
