# ccm — Claude Code session manager

A terminal UI for browsing and resuming your [Claude Code](https://claude.com/claude-code) sessions, with several sessions side by side in a tmux grid.

- Lists every session in `~/.claude/projects`, newest first, with project and title
- Click or press Enter to resume; sessions tile up to 4 per window
- Toggleable sessions sidebar inside a grid window
- Detail box shows the full title, folder and branch of the highlighted session (or the one under the mouse)
- Each pane gets its own colour; the focused pane is highlighted
- Notifications: when a session finishes or needs input while you're not looking at it, its pane gets a ✔ DONE / ⏳ NEEDS YOU badge, its window tab a ●, and Windows shows a toast (WSL)
- Runs on its own tmux server (`tmux -L ccm`), so your normal tmux setup is untouched

## Requirements

- tmux ≥ 3.2
- Python 3.8+ (standard library only)
- `claude` on your `PATH`

## Install

```bash
git clone https://github.com/lnnrcrrd/ccm.git
cd ccm && ./install.sh
ccm
```

## Keys

| Where | Key | Action |
|---|---|---|
| list / sidebar | type | filter by title, project or branch |
| list / sidebar | Enter / click | resume (or focus it if already open) |
| list / sidebar | Ctrl-N | new session: asks for a folder, with live folder suggestions (↑↓ pick, Tab accept) |
| list / sidebar | Ctrl-R | rescan sessions |
| list / sidebar | Esc | clear filter, then detach (list) or close (sidebar) |
| anywhere | F1 | sessions list |
| anywhere | F2 | zoom / unzoom pane |
| anywhere | F3 | next grid window |
| anywhere | F4 | close pane |
| grid | F5 | toggle sessions sidebar |

Run `ccm` again to re-attach; everything stays as you left it.

## Notifications

Add these Claude Code hooks to `~/.claude/settings.json` (merge with any existing ones):

```json
{
  "hooks": {
    "Stop": [{ "hooks": [{ "type": "command", "command": "~/.local/bin/ccm --notify 2>/dev/null || true", "async": true }] }],
    "Notification": [{ "hooks": [{ "type": "command", "command": "~/.local/bin/ccm --notify 2>/dev/null || true", "async": true }] }]
  }
}
```

The hook does nothing outside ccm. Badges clear when you focus the pane.

Toasts play ccm's own soft "blip" chimes (`sounds/done.wav`, `sounds/input.wav`, made by `tools/make_sounds.py`) instead of the Windows sound. Each chime starts with ~2.5 s of silence so Bluetooth headphones wake up before the blip plays. To use your own, drop `done.wav` / `input.wav` into `~/.config/ccm/`.

## Settings

| Variable | Default | Meaning |
|---|---|---|
| `CCM_PER_WINDOW` | 4 | sessions per grid window |
| `CCM_SIDEBAR_WIDTH` | 44 | sidebar width in columns |

These are read when the ccm tmux server starts (`tmux -L ccm kill-server` to restart it).
