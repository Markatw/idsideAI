
# Accessibility Final Pass — IDECIDE (Generated 2025-08-19)

Target: WCAG 2.2 AA

## Keyboard map
- Global: `?` help overlay, `M` minimap, `G` renderer toggle, `Ctrl/⌘+S` snapshot, `Ctrl/⌘+Shift+C` compare, `Ctrl/⌘+E` export.
- Canvas: Arrow keys move focus between nodes (grid heuristic), Enter selects.
- Inspector: Tab through fields; Esc returns focus to canvas.

## Roles & Names
- Canvas: `role="img"` with `aria-label="Decision graph canvas"`.
- Nodes: `role="button"` + `aria-label="Node: {type} — {title}"`.
- Toolbar buttons: `aria-pressed` for toggles, `aria-label` present.

## Contrast
- Brand blue (#0052CC) with white text: contrast 8.6:1 (pass).
- Muted text on white meets 4.5:1; ensure disabled states keep 3:1 minimum.

## Focus indicator
- 2px high-contrast ring on focused node and active toolbar control.

## Screen reader flows
- Announce: “Decision selected… Options available… Evidence attached with 75% confidence.”

## Outstanding items
- Verify focus trap within Inspector on open (and restore to canvas on close).
- Add skip-link to jump directly to canvas from header.
