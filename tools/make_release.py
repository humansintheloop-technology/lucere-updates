#!/usr/bin/env python3
"""Lucere updates: build, verify, and test releases.

  Add a release (copies files into releases/<version>/, fingerprints them, updates manifest.json):
    python3 tools/make_release.py add --version 1.7.1 --channel beta --from 1.7.0 \
        --title "..." --note "..." [--essential] [--touches-send | --send-unchanged] \
        [--capability "plain words"] --file path/to/17_x.py:page-patch [--file ...]

  Verify every fingerprint in manifest.json against the files here (run before every merge):
    python3 tools/make_release.py verify

  Test-apply every page patch from one version to the newest, on a real page:
    python3 tools/make_release.py try --page os-page.html --from 1.7.0 --channel beta

Rules it enforces, so a release stays small, readable, and safe to apply in an owner's chat:
  - files are plain ASCII, "\\n" line endings, no tabs, no trailing spaces, one final newline, under 16 KB;
  - only roles page-patch, doc, skill, instructions;
  - a page patch that mentions reply, mailSend, CAN_REPLY, sendReplies, capabilities, or a
    connector tool name must be marked --touches-send (shown to owners and asked separately)
    or --send-unchanged (you have read it and it does not change sending);
  - the full kit never goes here: no os-page.html, no project-instructions template with placeholders
    for install, and nothing that looks like a key or token.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, 'manifest.json')
SOURCE = 'https://raw.githubusercontent.com/humansintheloop-technology/lucere-updates/main/'
ROLES = {'page-patch', 'doc', 'skill', 'instructions'}
SEND_WORDS = re.compile(r"reply|mailSend|CAN_REPLY|sendReplies|capabilit|send_message|forward|create_event|update_tasks|web_fetch|web_search")
SECRET = re.compile(r"github_pat_|ghp_[A-Za-z0-9]{20}|gho_[A-Za-z0-9]{20}|sk-[A-Za-z0-9]{20}|BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}")
MAX_BYTES = 16 * 1024

def ver(v): return tuple(int(x) for x in v.lstrip('v').split('.'))
def sha(b): return hashlib.sha256(b).hexdigest()
def load():
    with open(MANIFEST, encoding='utf-8') as f: return json.load(f)
def save(m):
    with open(MANIFEST, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(m, indent=2, ensure_ascii=True) + '\n')

def check_text(path, raw):
    errs = []
    if len(raw) > MAX_BYTES: errs.append(f'{path}: {len(raw)} bytes, over {MAX_BYTES}')
    try: t = raw.decode('ascii')
    except UnicodeDecodeError: return errs + [f'{path}: not plain ASCII (write curly quotes as \\u2019 in Python strings)']
    if '\r' in t: errs.append(f'{path}: has \\r line endings')
    if '\t' in t: errs.append(f'{path}: has tabs')
    if any(l != l.rstrip(' ') for l in t.split('\n')): errs.append(f'{path}: trailing spaces')
    if not t.endswith('\n') or t.endswith('\n\n'): errs.append(f'{path}: must end with exactly one newline')
    if SECRET.search(t): errs.append(f'{path}: looks like it holds a key or token')
    if os.path.basename(path) in ('os-page.html',) or '<!DOCTYPE html>' in t: errs.append(f'{path}: a whole page never goes here; ship a patch')
    return errs

def cmd_add(a):
    m = load()
    if any(r['version'] == a.version for r in m['releases']): sys.exit(f'{a.version} is already released; versions are never reused')
    if a.channel not in ('beta', 'stable'): sys.exit('channel must be beta or stable')
    if a.touches_send and a.send_unchanged: sys.exit('choose one of --touches-send or --send-unchanged')
    newest = max((r['version'] for r in m['releases']), key=ver)
    if ver(a.version) <= ver(newest): sys.exit(f'{a.version} must be newer than {newest}')
    dest = os.path.join(ROOT, 'releases', a.version)
    files, errs, flagged = [], [], []
    for spec in a.file:
        src, _, role = spec.rpartition(':')
        if role not in ROLES: sys.exit(f'{spec}: role must be one of {sorted(ROLES)}')
        raw = open(src, 'rb').read()
        errs += check_text(src, raw)
        if role == 'page-patch' and SEND_WORDS.search(raw.decode('ascii', 'replace')): flagged.append(os.path.basename(src))
        sub = 'patches' if role == 'page-patch' else 'files'
        rel = f'releases/{a.version}/{sub}/{os.path.basename(src)}'
        files.append((src, rel, role, raw))
    if errs: sys.exit('Not released:\n  ' + '\n  '.join(errs))
    if flagged and not (a.touches_send or a.send_unchanged):
        sys.exit('These patches mention sending, capabilities, or connector tools: ' + ', '.join(flagged) +
                 '\nRead them, then add --touches-send (owners are told and asked separately) or --send-unchanged.')
    os.makedirs(dest, exist_ok=True)
    out = []
    for src, rel, role, raw in files:
        p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb') as f: f.write(raw)
        out.append({'path': rel, 'role': role, 'sha256': sha(raw), 'bytes': len(raw)})
    rel = {'version': a.version, 'channel': a.channel, 'date': datetime.date.today().isoformat(),
           'title': a.title, 'note': a.note, 'essential': bool(a.essential), 'from': getattr(a, 'from'),
           'kind': 'patches', 'touches_send': bool(a.touches_send), 'capabilities': a.capability or [],
           'files': out, 'notes': f'releases/{a.version}/NOTES.md'}
    m['releases'].insert(0, rel)
    m['channels']['beta'] = max(m['channels'].get('beta', '0.0.0'), a.version, key=ver)
    if a.channel == 'stable': m['channels']['stable'] = a.version
    save(m)
    with open(os.path.join(dest, 'NOTES.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f"# Lucere v{a.version}\n\n{a.title}\n\n{a.note}\n\n- Channel: {a.channel}\n- Applies to: v{getattr(a, 'from')}\n- Essential: {'yes' if a.essential else 'no'}\n- Changes sending: {'yes' if a.touches_send else 'no'}\n- New capabilities: {', '.join(a.capability) if a.capability else 'none'}\n")
    print(f'Added v{a.version} ({a.channel}). Now run: python3 tools/make_release.py verify')

def cmd_verify(a):
    m = load(); bad = []
    for k in ('channels', 'releases'):
        if k not in m: bad.append(f'manifest has no {k}')
    seen = set()
    for r in m.get('releases', []):
        if r['version'] in seen: bad.append(f"{r['version']} listed twice")
        seen.add(r['version'])
        for f in r.get('files', []):
            p = os.path.join(ROOT, f['path'])
            if not f['path'].startswith('releases/') or '..' in f['path']: bad.append(f"{f['path']}: outside releases/")
            if not os.path.exists(p): bad.append(f"{f['path']}: missing"); continue
            raw = open(p, 'rb').read()
            bad += check_text(f['path'], raw)
            if sha(raw) != f['sha256']: bad.append(f"{f['path']}: sha256 differs from the manifest")
            if len(raw) != f['bytes']: bad.append(f"{f['path']}: size differs from the manifest")
    for ch, v in m.get('channels', {}).items():
        if v not in seen: bad.append(f'channel {ch} points to {v}, which is not released')
    for dp, _, fs in os.walk(ROOT):
        if '.git' in dp: continue
        for fn in fs:
            p = os.path.join(dp, fn)
            try: t = open(p, encoding='utf-8').read()
            except Exception: continue
            if SECRET.search(t) and fn != 'make_release.py': bad.append(f'{os.path.relpath(p, ROOT)}: looks like it holds a key or token')
    if bad: sys.exit('FAIL\n  ' + '\n  '.join(bad))
    print(f"ok: {len(seen)} releases, every fingerprint matches, no keys")

def cmd_try(a):
    m = load(); cur = getattr(a, 'from'); page = open(a.page, encoding='utf-8').read()
    chain = sorted([r for r in m['releases'] if r['kind'] == 'patches' and ver(r['version']) > ver(cur)
                    and (a.channel == 'beta' or r['channel'] == 'stable')], key=lambda r: ver(r['version']))
    with tempfile.TemporaryDirectory() as d:
        cur_file = os.path.join(d, 'page.html'); open(cur_file, 'w', encoding='utf-8').write(page)
        for r in chain:
            if r['from'] != cur: sys.exit(f"v{r['version']} applies to v{r['from']}, but the page is on v{cur}")
            for f in r['files']:
                if f['role'] != 'page-patch': continue
                out = os.path.join(d, 'out.html')
                res = subprocess.run([sys.executable, '-I', os.path.join(ROOT, f['path']), cur_file, out], capture_output=True, text=True)
                if res.returncode: sys.exit(f"{f['path']} stopped:\n{res.stderr}")
                shutil.move(out, cur_file)
            got = re.search(r"const KIT_VERSION = '([\d.]+)'", open(cur_file, encoding='utf-8').read())
            if not got or got.group(1) != r['version']: sys.exit(f"after v{r['version']} the page says {got and got.group(1)}")
            cur = r['version']; print(f'ok: applied v{cur}')
        if a.out: shutil.copy(cur_file, a.out)
    print(f'ok: page is now v{cur}')

ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
p = sp.add_parser('add'); p.add_argument('--version', required=True); p.add_argument('--channel', required=True)
p.add_argument('--from', required=True); p.add_argument('--title', required=True); p.add_argument('--note', required=True)
p.add_argument('--essential', action='store_true'); p.add_argument('--touches-send', action='store_true')
p.add_argument('--send-unchanged', action='store_true'); p.add_argument('--capability', action='append')
p.add_argument('--file', action='append', required=True)
sp.add_parser('verify')
p = sp.add_parser('try'); p.add_argument('--page', required=True); p.add_argument('--from', required=True)
p.add_argument('--channel', default='beta'); p.add_argument('--out')
a = ap.parse_args(); {'add': cmd_add, 'verify': cmd_verify, 'try': cmd_try}[a.cmd](a)
