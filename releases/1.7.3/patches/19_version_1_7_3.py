"""Lucere v1.7.3 (beta): every update is tested before it reaches the page.
This page patch only raises the page's version to 1.7.3. The release also carries the project doc
os-regression-tests.md and the updated update and nightly skills, which run the regression test before
anything is published. Run: python3 19_version_1_7_3.py in.html out.html"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, 'expected one match (found %d) for: %s' % (n, old[:60])
    s = s.replace(old, new)


rep("const KIT_VERSION = '1.7.2';",
    "const KIT_VERSION = '1.7.3';")

open(dst, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
