import shlex
import shutil
from pathlib import Path
from subprocess import PIPE, Popen, run

from libqtile import qtile
from libqtile.log_utils import logger

from .colors import auto_color

CFG_ROOT = Path.home() / ".config/qtile"


class Program:
    cmd = None

    def __init__(self):
        self.name = self.__class__.__name__.lower()

    def kill(self):
        run(["pkill", self.name])

    def check(self):
        exists = shutil.which(self.name)
        if not exists:
            Popen(["notify-send", f"{self.name} does not exist"])

        return exists

    def run(self):
        self.kill()
        logger.warning(self.cmd)
        Popen(shlex.split(self.cmd))


class Dunst(Program):
    def run(self):
        self.kill()
        cat = Popen(
            ("cat", CFG_ROOT / "conf/dunstrc", CFG_ROOT / "colors/dunstrc"), stdout=PIPE
        )
        Popen(
            shlex.split(
                "dunst -conf -",
            ),
            stdin=cat.stdout,
        )


class Picom(Program):
    cmd = f'picom --config "{CFG_ROOT/ "conf/picom.conf"}" -b'


class Feh(Program):
    def __init__(self):
        self.cmd = "feh --bg-fill --randomize " + " ".join(self._get_files())
        super(Feh, self).__init__()

    @staticmethod
    def kill():
        pass

    @staticmethod
    def _get_files():
        wall_path = (CFG_ROOT / "wallpapers/current").resolve()
        files = []
        if wall_path.is_file():
            files.append(wall_path)
        elif wall_path.is_dir():
            files.extend(list(wall_path.iterdir()))
        return map(str, files)


class Eww(Program):
    def __init__(self):
        self.cmd = self._make_cmd()
        super(Eww, self).__init__()

    @staticmethod
    def _make_cmd():
        bars = ""
        for i in range(len(qtile.screens)):
            bars += f" bar{i}"
        return f"eww -c {CFG_ROOT / 'eww'} open-many {bars} --debug"


def autostart():
    auto_color()

    programs = [Dunst(), Picom(), Eww(), Feh()]

    for program in programs:
        if program.check():
            program.run()


if __name__ == "__main__":
    autostart()
