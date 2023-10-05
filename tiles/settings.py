import json
from pathlib import Path

from libqtile.utils import guess_terminal

try:
    with (Path.home() / ".config/qtile/colors/colors.json").open("r") as f:
        color = json.load(f)
except FileNotFoundError:
    color = {"name": "mauve", "hex": "#DDB6F2"}

mod = "mod4"
terminal = guess_terminal(["wezterm", "alacritty"])
cursor_warp = True
