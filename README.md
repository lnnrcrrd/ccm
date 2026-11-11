# ccm — Claude Code session manager

A terminal UI for browsing and resuming your [Claude Code](https://claude.com/claude-code) sessions, with several sessions side by side in a tmux grid.

- Lists every session in `~/.claude/projects`, newest first, with project and title
- Click or press Enter to resume; sessions tile up to 4 per window
- Toggleable sessions sidebar inside a grid window
- Each pane gets its own colour; the focused pane is highlighted
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
| list / sidebar | Ctrl-N | new session in the selected session's directory |
| list / sidebar | Ctrl-R | rescan sessions |
| list / sidebar | Esc | clear filter, then detach (list) or close (sidebar) |
| anywhere | F1 | sessions list |
| anywhere | F2 | zoom / unzoom pane |
| anywhere | F3 | next grid window |
| anywhere | F4 | close pane |
| grid | F5 | toggle sessions sidebar |

Run `ccm` again to re-attach; everything stays as you left it.

## Settings

| Variable | Default | Meaning |
|---|---|---|
| `CCM_PER_WINDOW` | 4 | sessions per grid window |
| `CCM_SIDEBAR_WIDTH` | 44 | sidebar width in columns |

These are read when the ccm tmux server starts (`tmux -L ccm kill-server` to restart it).
