import subprocess
from pathlib import Path

from libqtile import hook

from .state import State

state = State()
HOME = f"{Path.home()}/"


@hook.subscribe.startup
def autostart():
    subprocess.Popen([HOME + ".config/qtile/autostart.sh"])


@hook.subscribe.enter_chord
def notify_enter(chord_name):
    state.update_state({"chord": chord_name})
    subprocess.Popen(["notify-send", f"entered chord: {chord_name}"])


@hook.subscribe.leave_chord
def notify_exit():
    state.update_state({"chord": ""})
    subprocess.Popen(["notify-send", "exited chord"])


@hook.subscribe.layout_change
@hook.subscribe.client_new
@hook.subscribe.changegroup
@hook.subscribe.focus_change
async def _(*args):
    state.update_state()
