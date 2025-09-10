# ISDIDE Brand Tokens (Locked)

- **Primary Deep**: `#0B3D91` (var(--brand-blue-deep))
- **Primary Accent**: `#1E90FF` (var(--brand-blue-accent))
- **Background**: `#071A3C` (var(--bg))
- **Panel Surface**: `#0B275F` (var(--panel))
- **Foreground**: `#EAF2FF` (var(--fg))
- **Border**: `rgba(255,255,255,.08)` (var(--border))

Guidelines: No inline colors; use tokens only; navbar uses gradient(deep→accent);
panels/cards use var(--panel); maintain AA contrast.

**Enforcement:** No inline styles or raw hex colors in templates. Use CSS tokens and utility classes (e.g., `.hidden`).
## Iconography (Locked) — Sprint 18.1
- Success: gradient blue circle (#0B3D91→#1E90FF) with white check — `/static/icons/status-pass.svg`
- Fail: deep blue circle (#0B3D91) with white cross — `/static/icons/status-fail.svg`
- Warning: light blue circle (#1E90FF) with amber (!) — `/static/icons/status-warn.svg`
- Info: light blue circle (#1E90FF) with white “i” — `/static/icons/status-info.svg`
Usage: reference via CSS `.icon.status-*`; no inline SVG styling; no raw hex in templates.
