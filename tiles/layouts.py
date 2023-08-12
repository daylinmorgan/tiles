from libqtile.config import Match
from libqtile.layout import Floating, Max, MonadTall

from .palettes import catppuccin as ctp
from .settings import color

defaults = dict(
    border_width=2, border_focus=color["hex"], border_normal=ctp["overlay1"]
)

layouts = [
    MonadTall(margin=5, **defaults),
    Max(**defaults),
]

floating_layout = Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *Floating.default_float_rules,
        Match(wm_class="feh"),
        Match(wm_class="org.jabref.gui.MainApplication"),
        Match(title="Geneious Prime"),
    ],
    **defaults,
)
