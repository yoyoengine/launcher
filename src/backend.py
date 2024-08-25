"""
    This file is a part of yoyoengine. (https://github.com/yoyoengine/yoyoengine)
    Copyright (C) 2024  Ryan Zmuda

    Licensed under the MIT license. See LICENSE file in the project root for details.
"""

import io
import os
import tarfile
import requests
import json

def detect_platform():
    import platform
    return platform.system()

class YoyoEngineHubBackend:
    def __init__(self, version, hub_api_url, engine_api_url):
        self.platform = detect_platform()
        self.version = version

        self.hub_api_url = hub_api_url
        self.engine_api_url = engine_api_url

        self.available_cache = None
        self.update_hub_cache = None

    def check_for_hub_update(self) -> bool:
        # check the most recent release of yoyoengine and get its tag
        # compare the tag to the current version of the hub (ex: build 0 vs build 1)

        if(self.update_hub_cache is not None):
            return self.update_hub_cache

        res = json.loads(requests.get(f"{self.hub_api_url}/releases").text)
        latest_release_tag = res[0]['tag_name']

        self.update_hub_cache = (latest_release_tag != self.version)

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

    def check_remote_versions(self):
        # get all releases

        if(self.available_cache is not None):
            return self.available_cache

        res = json.loads(requests.get(f"{self.engine_api_url}/releases").text)
        versions = []
        for release in res:
            versions.append({
                "version": release['tag_name'],
                "url": release['html_url'],
                "date": release['published_at']
            })
        
        self.available_cache = versions

        return versions

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
        
    def install_by_tag(self, tag):
        print(f"Installing version {tag}")

        """
            Each yoyoengine release has files following this pattern:

            yoyoeditor-build**-linux-amd64.tar.gz
        
            we just need to download that and extract it into the editors directory
        """
        res = json.loads(requests.get(f"{self.engine_api_url}/releases/tags/{tag}").text)
        assets = res['assets']
        for asset in assets:
            if "yoyoeditor-build" in asset['name'] and self.platform in asset['name']:
                download_url = asset['browser_download_url']
                break

        # Define the path for the extraction
        editors_dir = os.path.expanduser("~/.local/share/yoyoengine/editors")
        tag_dir = os.path.join(editors_dir, tag)

        # Ensure the tag directory exists
        os.makedirs(tag_dir, exist_ok=True)

        # Download the tarball
        r = requests.get(download_url)
        tar = tarfile.open(fileobj=io.BytesIO(r.content))
        
        try:
            # Extract the tarball into the tag directory
            tar.extractall(path=tag_dir)
        finally:
            tar.close()

        print(f"Version {tag} installed successfully in {tag_dir}")

    # this is taking in the dict we give earlier, that has a path key
    def open_editor(self, version):
        # create a completely new proc to run the editor
        import subprocess
        subprocess.Popen([f"{version['path']}/yoyoeditor"], shell=True)

    def uninstall_editor(self, version):
        import shutil
        shutil.rmtree(version['path'])
    
    def uninstall_everything(self):
        import shutil
        shutil.rmtree(os.path.expanduser("~/.local/share/yoyoengine"))