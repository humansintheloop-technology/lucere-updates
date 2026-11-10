# Releasing a Lucere update

Every release is small, plain, and readable, because owners see its notes before they say yes, and Claude applies it in their chat.

## Before you start
- One change, one release. Keep each page patch under 16 KB and plain ASCII (inside a Python string, write a curly apostrophe as the escape `\u2019`).
- A page patch is a Python script run as `python3 <patch> in.html out.html`. It must assert the exact code it expects (one match, or stop), the way the kit's upgrade patches do. A page changed in chat then stops safely instead of breaking.
- Never put the whole page, the install kit, a key, or a token here.
- Big changes (new docs and instructions throughout) still go out as a zip by email. List them with `"kind": "by-email"` and no files.

## Steps
1. Write and test the patch against the current kit page (in the private kit repository): apply it, run the kit's tests, and raise `const KIT_VERSION` to the new version inside the same patch.
2. Make a branch here, then add the release:
   `python3 tools/make_release.py add --version 1.7.2 --channel beta --from 1.7.1 --title "..." --note "..." --file path/to/18_x.py:page-patch`
   - Title and note are what owners read. Plain words, one or two sentences, no jargon.
   - Add `--essential` only for a safety fix or something broken for everyone. It sits at the top of every brief until it's in.
   - If the patch mentions sending, capabilities, or a connector tool, the tool stops until you read it and add `--send-unchanged`, or `--touches-send` (owners are told and asked separately).
   - Add `--capability "plain words"` for anything the page would newly be allowed to do. It needs the owner's own yes.
3. Check it: `python3 tools/make_release.py verify`, and `python3 tools/make_release.py try --page <kit>/os-page.html --from <previous stable> --channel beta`.
4. Open a pull request. The check runs on it. Read the diff once more, then merge. Testers (beta) see it the next morning.
5. When it has run well for testers for a week, move it to stable: change `"channels": {"stable": ...}` and that release's `"channel"` to `"stable"` in a second pull request.
6. Never change or remove a released file. To fix a release, publish the next version.

## Keeping this repository safe
- Two-factor sign-in on every account with write access.
- Branch ruleset on `main`: pull request required, the "verify" check required, no force-push, no deletion.
- Tag ruleset on `v*`: no deletion or force-push.
- Few people with write access. Review `Settings, Collaborators` each quarter.
- If anything looks wrong, set both channels back to the last good version in one commit. Spaces only ever move forward on their owner's yes, so no one is changed by a bad release they haven't accepted.
