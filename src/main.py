"""
    This file is a part of yoyoengine. (https://github.com/yoyoengine/yoyoengine)
    Copyright (C) 2024  Ryan Zmuda

    Licensed under the MIT license. See LICENSE file in the project root for details.
"""

# note: when porting to windows, refer to <https://github.com/rdbende/Sun-Valley-ttk-theme>

from gui import YoyoEngineHub

# semver for hub
VERSION = "v1.0.0"
RELEASE = True

if __name__ == "__main__":

    # check for --dev
    import sys
    if "--dev" in sys.argv:
        RELEASE = False

    gui = YoyoEngineHub(VERSION, RELEASE)
    gui.run()