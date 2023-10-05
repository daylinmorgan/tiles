import json
from pathlib import Path

from libqtile import qtile

from .icons import icons


class State:
    def __init__(self) -> None:
        self.logfile = Path("/tmp/.qtile-state")
        self.logfile.touch()
        self.icons = icons
        self.layouts = {}

    def match_icon(self, window):
        for k, v in self.icons["icons"].items():
            if k in window or k == window:
                return v

    def get_icon(self, windows):
        matches = [self.match_icon(window) for window in windows]
        if not any(matches):
            return self.icons["busy"]
        elif len(matches) != len(windows):
            return self.icons["busy"]
        elif len(set(matches)) != 1:
            return self.icons["multi"]
        else:
            return matches[0]

    def get_layout(self, layout, windows):
        if layout == "max":
            return f"max ({len(windows)} )" if len(windows) > 1 else "max"
        else:
            return layout

    def get_group_state(self, name, info, index):
        g_state = {"name": name}
        if info["screen"] is not None:
            if info["screen"] == index:
                g_state["icon"] = ""
                g_state["status"] = "active"
                self.layouts[index] = self.get_layout(info["layout"], info["windows"])
            else:
                g_state["icon"] = self.get_icon(info["windows"])
                g_state["status"] = "busy"

        elif info["windows"]:
            g_state["icon"] = self.get_icon(info["windows"])

        else:
            g_state["icon"] = ""

        return g_state

    def get_state(self, update={}):
        screens = qtile.get_screens()
        groups = qtile.get_groups()
        screen_state = {}

        for s in screens:
            screen_state[s["index"]] = {"groups": [], "layout": ""}
            for g, info in groups.items():
                if g == "scratchpad":
                    continue

                g_state = self.get_group_state(g, info, s["index"])
                screen_state[s["index"]]["groups"].append(g_state)

            screen_state[s["index"]]["layout"] = self.layouts[s["index"]]

        self.state = {"screens": screen_state, "chord": "", **update}

    def write_state(self):
        with self.logfile.open("a") as f:
            f.write(json.dumps(self.state) + "\n")

    def update_state(self, update={}):
        self.get_state(update)
        self.write_state()
