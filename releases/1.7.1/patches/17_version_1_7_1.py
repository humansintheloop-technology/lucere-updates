"""Lucere v1.7.1 (beta, a test release): raises the page's version to 1.7.1, and nothing else.
It shows that updates reach a tester's space and apply on their yes.
Run: python3 17_version_1_7_1.py in.html out.html"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
old = "const KIT_VERSION = '1.7.0';"
n = s.count(old)
assert n == 1, 'expected the page to be on v1.7.0 (found %d)' % n
s = s.replace(old, "const KIT_VERSION = '1.7.1';")
open(dst, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
