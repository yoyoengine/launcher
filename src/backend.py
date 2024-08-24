"""
    This file is a part of yoyoengine. (https://github.com/zoogies/yoyoengine)
    Copyright (C) 2024  Ryan Zmuda

    Licensed under the MIT license. See LICENSE file in the project root for details.
"""

import os
import requests
import json

def detect_platform():
    import platform
    return platform.system()

class YoyoEngineHubBackend:
    def __init__(self, version):
        self.platform = detect_platform()
        self.version = version

        # self.api_url = "https://api.github.com/repos/yoyoengine/launcher"
        self.api_url = "https://api.github.com/repos/zoogies/Boneworks-Save-Manager"

    # def create_yoyoengine_dirs(self):

    """
        A little bit compilcated, since we only want to check for an update
        for the hub.

        I'm leaning towards every single build we release updates the whole
        stack of yoyoengine software, since they are all so tightly integrated.
    """
    def check_for_hub_update(self) -> bool:
        # check the most recent release of yoyoengine and get its tag
        # compare the tag to the current version of the hub (ex: build 0 vs build 1)
        res = json.loads(requests.get(f"{self.api_url}/releases").text)
        latest_release_tag = res[0]['tag_name']

        if latest_release_tag != self.version:
            print(f"New version of the hub available: {latest_release_tag}")
            return True

        return False

    def ensure_bootstrapped(self):
        # Hub is a standalone app, so if this is the
        # first time its being run, we need to make
        # all of the directories we expect.

        # top level share dir
        path = os.path.expanduser("~/.local/share/yoyoengine")
        if not os.path.exists(path):
            os.makedirs(path)
        
        # editors dir
        path = os.path.expanduser("~/.local/share/yoyoengine/editors")
        if not os.path.exists(path):
            os.makedirs(path)


    def check_installed_versions(self):
        if self.platform == "Linux":
            import os
            # import sys
    
            path = os.path.expanduser("~/.local/share/yoyoengine/editors")
            if not os.path.exists(path):
                os.makedirs(path)
                return []
    
            dirs = os.listdir(path)
            versions = []
            for dir_name in dirs:
                dir_path = os.path.join(path, dir_name)
                if os.path.isdir(dir_path):
                    versions.append({
                        "version": dir_name,
                        "path": dir_path
                    })
            return versions
# # function which uses the github API to get a list of all releases for zoogies/yoyoengine
# def get_releases():
#     import requests
#     import json

#     url = "https://api.github.com/repos/zoogies/yoyoengine/releases"
#     response = requests.get(url)
#     releases = json.loads(response.text)
#     return releases

"""
    Spec:
    Linux:
        ~/.local/share/yoyoengine/ has
        /VERSION_NAME
        /VERSION_NAME
        for each editor installed

        inside of each is the full install for that version
"""
