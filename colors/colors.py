#!/usr/bin/env python3

import json
import os
import random
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

import tomli

SCRIPTDIR = Path(__file__).parent


@dataclass
class Current:
    name: str
    hex: str

    @classmethod
    def get(cls):
        if (SCRIPTDIR / "colors.json").is_file():
            with (SCRIPTDIR / "colors.json").open("r") as f:
                return cls(**json.load(f))
        else:
            return cls("rosewater", "#F5E0DC")

    def set(self, name, pal):
        self.name = name
        self.hex = pal[name]
        with (SCRIPTDIR / "colors.json").open("w") as f:
            json.dump(self.__dict__, f)


with (SCRIPTDIR / "config.toml").open("rb") as f:
    config = tomli.load(f)

current = Current.get()
pal = config["palette"]


def write_style(template, outfile, colors):
    with (SCRIPTDIR / outfile).open("w") as f:
        f.write(template.format(**colors))


def apply_style(color):
    current.set(color, pal)

    for info in config["pkgs"].values():
        write_style(
            template=info["template"],
            outfile=info["file"],
            colors={"primary": pal[color]},
        )


# ? do i need to use sys.stdout?
def echo(txt, newline=True):
    sys.stdout.write(txt + "\n" if newline else "")


def set_color(color, quit=False):
    apply_style(color)
    # rofi was catching xdotool key press so use qtile cmd
    subprocess.run(["qtile", "cmd-obj", "-o", "cmd", "-f", "reload_config"])
    echo("\x00data\x1f{color}\n".format(color=color))
    if not quit:
        menu(color)


def menu(selected):

    # add theme/config metadata to rofi
    echo(
        dedent(
            """
    \0theme\x1finputbar {{ border-color: {color};}}
    \0theme\x1fwindow {{ border-color: {color};}}
    \0theme\x1felement selected normal{{ background-color: {color};}}
    \0keep-selection\x1ftrue
    \0no-custom\x1ftrue
    \0message\x1fcurrent color: <b>{name}</b>
    """
        ).format(color=pal[selected], name=selected)
    )

    for color in pal:
        echo(color)

    echo("apply")
    echo("apply & quit")
    echo("quit")


def rofi():
    prev = os.getenv("ROFI_DATA") if os.getenv("ROFI_DATA") else current.name
    selected = sys.argv[1] if len(sys.argv) != 1 else current.name

    # give rofi new data
    echo("\x00data\x1f{selected}\n".format(selected=selected))

    if "apply" in selected:
        set_color(prev, quit=("quit" in selected))
    elif selected == "quit":
        sys.exit()
    else:
        menu(selected)


def no_rofi():
    if len(sys.argv) > 1:
        if sys.argv[1] in pal:
            apply_style(sys.argv[1])
        else:
            print(f"ERROR. Unknown color: {sys.argv[1]}")
            print("Must be one of: ")
            print("\n".join(pal))
    else:
        color = random.choice(list(pal))
        print(f"no color specified...using {color}")
        print("reset your wm to apply the changes")
        apply_style(color)


if __name__ == "__main__":
    if not os.getenv("ROFI_OUTSIDE"):
        no_rofi()
    else:
        rofi()
