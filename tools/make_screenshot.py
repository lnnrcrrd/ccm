#!/usr/bin/env python3
"""Draw docs/screenshot.svg: a mock of ccm (sidebar + 2x2 grid) with made-up sessions."""
from pathlib import Path
from xml.sax.saxutils import escape

CW, LH = 8.4, 18                      # char width / line height (px) for 14px monospace
COLS, ROWS = 150, 40
W, H = int(COLS * CW), ROWS * LH
BG, FG, DIM, ORANGE = "#1e1f29", "#d8d8e0", "#7a7c8c", "#ffaf00"
out = []


def text(col, row, s, fill=FG, bold=False, bg=None):
    x, y = col * CW, row * LH
    if bg:
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{len(s) * CW:.1f}" height="{LH}" fill="{bg}"/>')
    w = ' font-weight="bold"' if bold else ""
    out.append(f'<text x="{x:.1f}" y="{y + 13}" fill="{fill}"{w} xml:space="preserve">{escape(s)}</text>')


def hline(col, row, n, color):
    text(col, row, "━" * n, color)


def vline(col, r0, r1, color):
    for r in range(r0, r1):
        text(col, r, "┃", color)


SIDE = 44
# ---- sidebar ------------------------------------------------------------
text(0, 0, " ● sessions ", "#1e1f29", True, "#bcbcbc")
text(0, 1, " Claude sessions (64/64)   filter: ▏", FG, True)
rows = [("●", "now", "api", "Refactor auth middleware"), ("✔", "2m", "web", "Fix flaky checkout test"),
        ("⏳", "5m", "infra", "Terraform plan for staging"), ("●", "8m", "docs", "Write onboarding guide"),
        (" ", "1h", "api", "Add rate limiting to search"), (" ", "3h", "web", "Dark mode toggle"),
        (" ", "5h", "~", "Dotfiles cleanup"), (" ", "1d", "data", "Nightly ETL timeout"),
        (" ", "2d", "api", "Pagination for /orders"), (" ", "3d", "mobile", "Push notification opt-in"),
        (" ", "4d", "web", "Upgrade to React 19"), (" ", "1w", "infra", "Rotate CI secrets"),
        (" ", "1w", "data", "Backfill customer metrics"), (" ", "2w", "~", "Shell prompt tweaks")]
mark_color = {"●": "#5fd75f", "✔": "#5fd75f", "⏳": "#ffd75f"}
for i, (m, age, proj, title) in enumerate(rows):
    r = 2 + i
    sel = i == 1
    if sel:
        text(0, r, " " * (SIDE - 1), FG, False, "#d0d0d0")
    ink = "#1e1f29" if sel else None
    if m != " ":
        text(1, r, m, ink or mark_color[m])
    text(3, r, f"{age:>4}", ink or FG)       # each column drawn on its own so glyph widths can't drift
    text(9, r, proj, ink or ORANGE)
    text(21, r, title[:SIDE - 22], ink or FG)
text(0, ROWS - 8, "─" * (SIDE - 1), DIM)
text(1, ROWS - 7, "Fix flaky checkout test: retry the", FG, True)
text(1, ROWS - 6, "payment iframe wait and stub Stripe", FG, True)
text(1, ROWS - 5, "~/code/web · fix/checkout-flake · 2m ago", ORANGE)
text(0, ROWS - 3, " ⏎/double-click open · ^N new · Esc close", DIM)
vline(SIDE, 0, ROWS - 1, "#444")

# ---- 2x2 grid ------------------------------------------------------------
gx, gw = SIDE + 1, COLS - SIDE - 1
pw, ph = (gw - 1) // 2, (ROWS - 2) // 2
panes = [
    (0, 0, "#00afff", "#005f87", "Refactor auth middleware", "active", [
        ("● ", "Updated src/middleware/auth.ts", FG), ("  ⎿ ", "+42 −18 lines", DIM),
        ("● ", "Running npm test -- auth", FG), ("  ⎿ ", "✓ 37 passed (1.8s)", "#5fd75f"), ("", "", FG),
        ("● ", "The middleware now validates tokens once per", FG),
        ("  ", "request and caches the decoded claims.", FG), ("", "", FG), ("> ", "▏", FG)]),
    (1, 0, "#87d787", "#5f875f", "Fix flaky checkout test", "done", [
        ("● ", "Root cause: the payment iframe loads after", FG), ("  ", "the 2s default wait.", FG), ("", "", FG),
        ("● ", "Updated e2e/checkout.spec.ts", FG), ("  ⎿ ", "+9 −3 lines", DIM),
        ("● ", "Ran it 20× in a row: 20/20 green.", "#5fd75f"), ("", "", FG), ("> ", "", FG)]),
    (0, 1, "#d787d7", "#875f87", "Terraform plan for staging", "input", [
        ("● ", "Plan: 3 to add, 1 to change, 0 to destroy.", FG), ("", "", FG),
        ("  ", "Do you want to run terraform apply?", "#ffd75f"),
        ("  ", "❯ 1. Yes", FG), ("  ", "  2. No, show me the diff first", FG)]),
    (1, 1, "#ffaf5f", "#af5f00", "Write onboarding guide", "", [
        ("● ", "Reading docs/ and the last 30 PRs…", FG), ("", "", FG),
        ("✻ ", "Drafting… (14s · ↓ 1.2k tokens)", "#ffaf5f")]),
]
for cx, cy, bright, dim, title, state, body in panes:
    c0, r0 = gx + cx * (pw + 1), cy * (ph + 1)
    if state == "active":
        bar = f" ▶ {title} "
        text(c0, r0, bar, "#1e1f29", True, bright)
        hline(c0 + len(bar), r0, pw - len(bar), bright)
    else:
        col = c0
        if state == "done":
            text(col, r0, " ✔ DONE ", "#1e1f29", True, "#00d75f"); col += 8
        if state == "input":
            text(col, r0, " ⏳ NEEDS YOU ", "#1e1f29", True, "#ffd700"); col += 13
        t = f" {title} "
        text(col, r0, t, "#e4e4e4", False, dim)
        hline(col + len(t), r0, pw - (col - c0) - len(t), dim)
    for i, (pre, msg, color) in enumerate(body):
        text(c0 + 1, r0 + 2 + i, pre, "#5fd75f" if pre.strip() == "●" else DIM)
        text(c0 + 1 + len(pre), r0 + 2 + i, msg, color)
vline(gx + pw, 1, ROWS - 1, "#00afff")
hline(gx, ph, gw, "#444")

# ---- status bar ----------------------------------------------------------
sb = ROWS - 1
text(0, sb, " " * COLS, FG, False, "#303030")
text(0, sb, " ccm ", FG, True, "#303030")
text(6, sb, " 0:sessions ", "#bcbcbc", False, "#303030")
text(18, sb, " 1:grid● ", "#1e1f29", True, "#ffaf00")
hint = " F1 sessions · F2 zoom · F4 close · F5 sidebar · F6/Alt+←→ switch "
text(COLS - len(hint), sb, hint, "#bcbcbc", False, "#303030")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="14">'
       f'<rect width="{W}" height="{H}" rx="8" fill="{BG}"/>' + "".join(out) + "</svg>")
dst = Path(__file__).resolve().parent.parent / "docs" / "screenshot.svg"
dst.write_text(svg)
print("wrote", dst, f"{W}x{H}")
