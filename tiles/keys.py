from collections import namedtuple
from pathlib import Path

from libqtile.config import EzKey, Key, KeyChord
from libqtile.lazy import lazy

from .settings import mod, terminal

HOME = f"{Path.home()}"
ROFI_BIN = f"{Path(__file__).parent.parent / 'rofi/bin'}"
EZKEY_MAP = {"M": "Super", "A": "Alt", "C": "Control", "S": "Shift"}

EzKeyDef = namedtuple("EzKeyDef", "combo cmd desc", defaults=(None,))
KeyDef = namedtuple("KeyDef", "mod key cmd desc", defaults=(None,))


def normalize_key(key):
    return key.replace("<", "").replace(">", "").capitalize() if len(key) > 1 else key


def get_ezkey_combo(key):
    return " + ".join(
        [EZKEY_MAP[m] if m in EZKEY_MAP else normalize_key(m) for m in key.split("-")]
    )


def get_key_combo(mods, key):
    return " + ".join(
        [mod.capitalize() if mod != "mod4" else "Super" for mod in mods]
        + [normalize_key(key)]
    )


def get_key_chord_help(mode, kc_def):
    key_help = []
    key_chord_combo = get_key_combo(kc_def["mods"], kc_def["key"])
    for k in kc_def["submappings"]:
        # only add if desc is not empty
        if k.desc:
            key_combo = f"{key_chord_combo} {k.key}"
            key_help.append(f"{key_combo:<25} {mode}: {k.desc}")
    # add in the rofi keybindings helpk key
    if mode == "rofi":
        key_combo = f"{key_chord_combo} k"
        key_help.append(f"{key_combo:<25} {mode}: show keybindings")
    return key_help


# just for displaying in the keybindings help
def show_key_help(keys, chords):
    key_help = []
    for k in keys:
        key_help.append(f"{get_ezkey_combo(k[0]):<25} {k[2]}")
    for mode, kc_def in chords.items():
        key_help.extend(get_key_chord_help(mode, kc_def))
    return "\n".join(key_help)


def dummy_key_chord_keys(mode, key_defs):
    all_letters = {chr(i) for i in range(ord("a"), ord("z") + 1)}
    used_letters = {key.key for key in key_defs}
    letters = all_letters.difference(used_letters)
    return [
        Key(
            [],
            letter,
            lazy.spawn(
                f"notify-send 'Key Error!' 'letter: {letter} not used in key chord mode: {mode}'"
            ),
        )
        for letter in letters
    ]


def make_key_chord(key_chord_dict):
    key_chords = []
    for mode, chord_def in key_chord_dict.items():
        key_chords.append(
            KeyChord(
                chord_def["mods"],
                chord_def["key"],
                [
                    Key(key.mod, key.key, key.cmd, lazy.ungrab_chord(), desc=key.desc)
                    for key in chord_def["submappings"]
                ]
                + dummy_key_chord_keys(mode, chord_def["submappings"]),
                mode=True,
                name=mode,
            )
        )
    return key_chords


main_key_defs = [
    # focus / layout
    EzKeyDef("M-h", lazy.prev_screen(), "move focus to prev screen"),
    EzKeyDef("M-l", lazy.next_screen(), "move focus to next screen"),
    EzKeyDef("M-j", lazy.layout.down(), "move focus down"),
    EzKeyDef("M-k", lazy.layout.up(), "move focus up"),
    EzKeyDef("M-<space>", lazy.layout.next(), "move window focus to other window"),
    EzKeyDef("M-<Tab>", lazy.next_layout(), "toggle between layouts"),
    # windows
    EzKeyDef("M-f", lazy.window.toggle_fullscreen(), "make window fullscreen"),
    EzKeyDef("M-S-f", lazy.window.toggle_floating(), "toggle floating window"),
    EzKeyDef("M-S-h", lazy.layout.shuffle_left(), "move window to the left"),
    EzKeyDef("M-S-l", lazy.layout.shuffle_right(), "move window to the right"),
    EzKeyDef("M-S-j", lazy.layout.shuffle_down(), "move window down"),
    EzKeyDef("M-S-k", lazy.layout.shuffle_up(), "move window up"),
    EzKeyDef("M-S-h", lazy.layout.swap_left(), "swap window left"),
    EzKeyDef("M-S-l", lazy.layout.swap_right(), "swap window right"),
    EzKeyDef("M-S-j", lazy.layout.shuffle_down(), "shuffle window down"),
    EzKeyDef("M-S-k", lazy.layout.shuffle_up(), "shuffle window up"),
    EzKeyDef("M-i", lazy.layout.grow(), "grow window"),
    EzKeyDef("M-m", lazy.layout.shrink(), "shrink window"),
    EzKeyDef("M-n", lazy.layout.normalize(), "normalize windows"),
    EzKeyDef("M-o", lazy.layout.maximize(), "maximize windows"),
    EzKeyDef("M-S-<space>", lazy.layout.flip(), "flip window"),
    EzKeyDef("M-S-q", lazy.window.kill(), "Kill focused window"),
    # Qtile
    EzKeyDef("M-S-r", lazy.restart(), "restart qtile"),
    EzKeyDef("M-C-r", lazy.reload_config(), "reload the config"),
    EzKeyDef("M-S-x", lazy.shutdown(), "shutdown qtile"),
    # Programs
    EzKeyDef("M-S-<Return>", lazy.spawn(terminal), "launch terminal"),
    EzKeyDef("M-p", lazy.spawn(f"{ROFI_BIN}/launcher.sh"), "show app launcher"),
    EzKeyDef("M-S-e", lazy.spawn("thunar"), "launch thunar"),
    EzKeyDef("M-C-l", lazy.spawn(f"{HOME}/bin/lock"), "lock the screen"),
    EzKeyDef("M-s", lazy.spawn("flameshot gui"), "take screenshot"),
    EzKeyDef(
        "M-S-s",
        lazy.spawn("flameshot screen -n 0"),
        "take screenshot of full screen",
    ),
    # Scratchpad
    EzKeyDef(
        "M-t",
        lazy.group["scratchpad"].dropdown_toggle("scratch term"),
        "Show terminal scratchpad",
    ),
    EzKeyDef(
        "M-C-k",
        lazy.spawn(f"feh {HOME}/home/daylin/crkbd-keyboard.png"),
        "Show crkbd keyboard layout",
    ),
]

system_key_defs = [
    EzKeyDef("<XF86AudioLowerVolume>", lazy.spawn("amixer set 'Master' 5%-")),
    EzKeyDef("<XF86AudioRaiseVolume>", lazy.spawn("amixer set 'Master' 5%+")),
    EzKeyDef("<XF86AudioMute>", lazy.spawn("amixer sset 'Master' toggle")),
    EzKeyDef("<XF86MonBrightnessUp>", lazy.spawn("light -A 5")),
    EzKeyDef("<XF86MonBrightnessDown>", lazy.spawn("light -U 5")),
]


key_chords_defs = {
    "rofi": {
        "mods": [mod],
        "key": "r",
        "submappings": [
            KeyDef([], "b", lazy.spawn(f"{ROFI_BIN}/bluetooth.sh"), "control bluetooth"),
            KeyDef([], "p", lazy.spawn(f"{ROFI_BIN}/powermenu.sh"), "show powermenu"),
            KeyDef([], "w", lazy.spawn(f"{ROFI_BIN}/windows.sh"), "show window picker"),
            KeyDef([], "s", lazy.spawn(f"{ROFI_BIN}/ssh.sh"), "show ssh picker"),
            KeyDef(
                [], "c", lazy.spawn(f"{ROFI_BIN}/colors.sh"), "show primary color picker"
            ),
        ],
    }
}

# only defined for use in the key bindings helper
group_keys_def = [
    EzKeyDef("M-#", "", "switch to group #"),
    EzKeyDef("M-S-#", "", "switch to & move focused window to group #"),
    EzKeyDef("M-C-#", "", "move focused window to group #"),
]

rofi_key_bindings_help = KeyDef(
    [],
    "k",
    lazy.spawn(
        "bash -c 'echo \""
        + show_key_help(main_key_defs + group_keys_def, key_chords_defs)
        + f'" | rofi -dmenu -i -p "Keyboard shortcuts" -theme {HOME}/.config/qtile/rofi/styles/keymap.rasi\''
    ),
    "Show keybindings help",
)

# generate keys
main_keys = [EzKey(key.combo, key.cmd, desc=key.desc) for key in main_key_defs]
system_keys = [
    EzKey(
        *key,
    )
    for key in system_key_defs
]

# add the keybinding helper
key_chords_defs["rofi"]["submappings"].append(rofi_key_bindings_help)
key_chords = make_key_chord(key_chords_defs)
keys = main_keys + key_chords + system_keys
