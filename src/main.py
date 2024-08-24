"""
    This file is a part of yoyoengine. (https://github.com/zoogies/yoyoengine)
    Copyright (C) 2024  Ryan Zmuda

    Licensed under the MIT license. See LICENSE file in the project root for details.
"""

# note: when porting to windows, refer to <https://github.com/rdbende/Sun-Valley-ttk-theme>

from gui import YoyoEngineHub

# semver for hub
VERSION = "v1.3" # TODO: fix before release

if __name__ == "__main__":
    # TODO: gui sometime in the future
    gui = YoyoEngineHub(VERSION)
    gui.run()