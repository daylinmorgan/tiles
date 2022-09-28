from libqtile import bar, qtile
from libqtile.config import DropDown, Group, Key, Match, ScratchPad, Screen
from libqtile.lazy import lazy

from .keys import keys
from .settings import mod, terminal

groups = [Group(i) for i in "12345678"] + [
    Group("9", matches=[Match(wm_class="Wavebox")])
]

for i in groups:
    keys.extend(
        [
            # mod + letter of group:
            # switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="switch to group {}".format(i.name),
            ),
            # mod + shift + letter of group:
            # switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="switch to & move focused window to group {}".format(i.name),
            ),
            # mod + ctrl + letter of group:
            # move focused window to group and don't switch
            Key(
                [mod, "control"],
                i.name,
                lazy.window.togroup(i.name),
                desc="move focused window to group {}".format(i.name),
            ),
        ]
    )
# add scratchpad
groups += groups + [
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "scratch term",
                terminal,
                x=0.1,
                y=0.1,
                width=0.8,
                height=0.8,
                opacity=0.9,
                on_focus_lost_hide=True,
            ),
        ],
    )
]
screens = [Screen(bar.Gap(45)) for _ in range(len(qtile.cmd_screens()))]
