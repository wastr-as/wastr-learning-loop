# Drop meeting recordings here

Put recordings in the matching context subfolder, then transcribe by name:

```powershell
# input/founders/standup.m4a
py transcribe.py standup.m4a

# input/customer/acme-call.m4a
py transcribe.py acme-call.m4a --context customer

# input/partner/hauler-call.m4a
py transcribe.py hauler-call.m4a --context partner
```

A bare filename is resolved against `input/<context>/` first, then `input/`.
You can still pass a full path to a file anywhere.

Recordings are git-ignored (captured in Notion, not committed here) — only these
`README.md` / `.gitkeep` placeholders are tracked.
