"""
    This file is a part of yoyoengine. (https://github.com/zoogies/yoyoengine)
    Copyright (C) 2024  Ryan Zmuda

    Licensed under the MIT license. See LICENSE file in the project root for details.
"""

# note: when porting to windows, refer to <https://github.com/rdbende/Sun-Valley-ttk-theme>

from gui import YoyoEngineHub

VERSION = "build 0"

# HEADER = '\033[95m'
# OKBLUE = '\033[94m'
# OKCYAN = '\033[96m'
# OKGREEN = '\033[92m'
# WARNING = '\033[93m'
# FAIL = '\033[91m'
# ENDC = '\033[0m'
# BOLD = '\033[1m'
# UNDERLINE = '\033[4m'

if __name__ == "__main__":
    # TODO: gui sometime in the future
    gui = YoyoEngineHub(VERSION)
    gui.run()

#     print(r"""
# Yb  dP  dP"Yb  Yb  dP  dP"Yb  888888 88b 88  dP""b8 88 88b 88 888888     88  88 88   88 88""Yb 
#  YbdP  dP   Yb  YbdP  dP   Yb 88__   88Yb88 dP   `" 88 88Yb88 88__       88  88 88   88 88__dP 
#   8P   Yb   dP   8P   Yb   dP 88""   88 Y88 Yb  "88 88 88 Y88 88""       888888 Y8   8P 88""Yb 
#  dP     YbodP   dP     YbodP  888888 88  Y8  YboodP 88 88  Y8 888888     88  88 `YbodP' 88oodP 
# """)
    
#     print(f"YoyoEngine Hub {OKGREEN} {VERSION} {ENDC}")
#     print("Ryan Zmuda - 2024")
#     print()

#     running = True
#     menu = "actions"
#     while running:
#         if(menu == "actions"):
#             print("Actions:")
#             print("1. Check for updates")
#             print("2. Exit")
#             print()
#             action = input("Select an action: ")

#             if(action == "1"):
#                 print("Checking for updates...")