# Lucere updates

This repository holds updates for Lucere, a personal operating system that each owner runs inside their own Claude account. It holds updates only. The full kit is not here.

## How an owner's space uses it
- Once a day, the owner's space reads `manifest.json` from this repository, and nothing else. It only reads. If a newer version is waiting, the owner's morning brief says so in one line.
- Nothing is applied until the owner says "update Lucere" in their own Claude project chat and then yes.
- Every file is checked against the size and sha256 fingerprint in `manifest.json` before it is used. If anything doesn't match, nothing changes.
- An update never adds a connection, a capability, a way to send, or a schedule on its own. If one would, it says so in plain words and asks the owner separately.
- The owner can say "go back to v<version>" at any time.

## What's here
- `manifest.json`: the channels (`stable`, and `beta` for early testers) and every release, newest first.
- `releases/<version>/`: each release's notes and its small files (page patches, and sometimes docs or skills).
- `tools/make_release.py`: builds, verifies, and test-applies releases. See RELEASING.md.

Questions or problems: owners say "Report a problem" in their project chat.
