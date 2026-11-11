#!/usr/bin/env bash
# Symlink ccm into place so edits in this repo take effect immediately.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
command -v tmux >/dev/null || { echo "tmux is required (>= 3.2)"; exit 1; }
mkdir -p ~/.local/bin ~/.config/ccm
ln -sf "$here/bin/ccm" ~/.local/bin/ccm
ln -sf "$here/config/tmux.conf" ~/.config/ccm/tmux.conf
echo "installed: run 'ccm' (make sure ~/.local/bin is on your PATH)"
