import json
import random
from dataclasses import dataclass
from pathlib import Path

CLR_CFG = Path.home() / ".config/qtile/colors"

with (CLR_CFG / "config.json").open("rb") as f:
    config = json.load(f)


@dataclass
class Current:
    name: str
    hex: str

    @classmethod
    def get(cls):
        if (CLR_CFG / "colors.json").is_file():
            with (CLR_CFG / "colors.json").open("r") as f:
                return cls(**json.load(f))
        else:
            return cls("rosewater", "#F5E0DC")

    def set(self, name, pal):
        self.name = name
        self.hex = pal[name]
        with (CLR_CFG / "colors.json").open("w") as f:
            json.dump(self.__dict__, f)


def write_style(template, outfile, colors):
    with (CLR_CFG / outfile).open("w") as f:
        f.write(template.format(**colors))


current = Current.get()
pal = config["palette"]


def apply_style(color):
    current.set(color, pal)

    for info in config["pkgs"].values():
        write_style(
            template=info["template"],
            outfile=info["file"],
            colors={"primary": pal[color]},
        )


def auto_color():
    if not (CLR_CFG / "colors.json").is_file():
        color = random.choice(list(pal))
        apply_style(color)
