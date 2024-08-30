"""
    This file is a part of yoyoengine. (https://github.com/yoyoengine/yoyoengine)
    Copyright (C) 2024  Ryan Zmuda

    Licensed under the MIT license. See LICENSE file in the project root for details.
"""

import tkinter as tk
from tkinter import ttk
import sv_ttk
import webbrowser
from backend import YoyoEngineHubBackend
from desktop_notifier import DesktopNotifier, Icon
from desktop_notifier.sync import DesktopNotifierSync

import asyncio
import os
import sys

from datetime import datetime, timezone
from dateutil import parser
from dateutil.relativedelta import relativedelta

def time_ago(timestamp_str):
    # Parse the timestamp string
    timestamp = parser.isoparse(timestamp_str)
    now = datetime.now(timezone.utc)  # Make `now` timezone-aware

    # Calculate the difference
    delta = relativedelta(now, timestamp)

    # Format the difference
    if delta.years > 0:
        return f"{delta.years} years ago"
    elif delta.months > 0:
        return f"{delta.months} months ago"
    elif delta.days > 0:
        return f"{delta.days} days ago"
    elif delta.hours > 0:
        return f"{delta.hours} hours ago"
    elif delta.minutes > 0:
        return f"{delta.minutes} minutes ago"
    else:
        return "just now"

class YoyoEngineHub:
    def __init__(self, version, is_release, hub_api_url="https://api.github.com/repos/yoyoengine/launcher", editor_api_url="https://api.github.com/repos/yoyoengine/yoyoeditor"):
        self.notifier = DesktopNotifierSync(app_name="YoyoEngine Hub")
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("YoyoEngine Hub")
        self.tab = "editors"
        self.version = version
        self.backend = YoyoEngineHubBackend(version, hub_api_url, editor_api_url)

        try:
            self.update_available = self.backend.check_for_hub_update()
        except Exception as e:
            self.update_available = False

        self.is_release = is_release

        def path(src):
            if self.is_release:
                try:
                    base_path = sys._MEIPASS
                except Exception:
                    base_path = os.path.abspath(".")

                return os.path.join(base_path, src)
            else:
                # return f"../media/{src}"
                return f"media/{src}"

        self.version_logo = tk.PhotoImage(file=path("smallcleanlogo.png"))
        self.smallesttextlogo = tk.PhotoImage(file=path("smallesttextlogo.png"))
        self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file=path('cleanlogo.png')))

        if self.update_available:
            self.show_update_notification()
        else:
            self.platform = self.backend.platform
            if self.platform != "Linux":
                self.show_platform_error()
            else:
                self.hub()

    def show_update_notification(self):
        url = "https://github.com/yoyoengine/launcher/releases/latest"
        
        def open_update():
            webbrowser.open(url)
        
        def ignore_update():
            self.update_available = False
            self.clear()
            self.hub()

        notification_label = ttk.Label(self.root, text="An update is available!", font=("Roboto", 16))
        notification_label.grid(row=0, column=0, columnspan=2, pady=10)

        ignore_button = ttk.Button(self.root, text="Ignore", width=50, command=ignore_update)
        ignore_button.grid(row=1, column=0, padx=5, pady=5)

        install_button = ttk.Button(self.root, text="Install", width=50, command=open_update)
        install_button.grid(row=1, column=1, padx=5, pady=5)

        self.configure_grid(self.root, [0, 1], [0, 1])

    def show_platform_error(self):
        self.clear()
        frame = tk.Frame(self.root, width=300, height=300)
        frame.pack()
        error_txt = ttk.Label(frame, text='This program only works on Linux.')
        error_txt.pack()

    def hub(self):
        self.clear()
        self.configure_root_grid()
        self.create_top_bar()
        self.create_left_menu()
        self.create_content_area()
        self.bind_mouse_events()

        if self.tab == "editors":
            self.populate_editors_tab()
        elif self.tab == "settings":
            self.populate_settings_tab()

    def configure_root_grid(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=20)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)

    def create_top_bar(self):
        self.top_bar = tk.Frame(self.root)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        # self.top_bar.columnconfigure(0, weight=1)
        self.logo_label = tk.Label(self.top_bar, image=self.smallesttextlogo)
        self.logo_label.grid(row=0, column=0, pady=0, padx=10, sticky="nw")

        # to the right of this logo, aligned to the bottom we want version text self.version
        self.version_label = tk.Label(self.top_bar, text=f"hub {self.version}", fg="white", font=("Roboto", 10))
        self.version_label.grid(row=0, column=1, pady=0, padx=10, sticky="w")

    def create_left_menu(self):
        self.left_menu = tk.Frame(self.root)
        self.left_menu.grid(row=1, column=0, sticky="nsew")
        self.left_menu.columnconfigure(0, weight=1)
        self.left_menu.rowconfigure(2, weight=1)

        self.create_sidebar_buttons()
        self.create_footer()

    def create_sidebar_buttons(self):
        def open_editors():
            self.tab = "editors"
            self.clear()
            self.hub()

        def open_settings():
            self.tab = "settings"
            self.clear()
            self.hub()

        if self.tab == "editors":
            self.editors_btn = ttk.Button(self.left_menu, text="Editors", state="disabled")
            self.settings_btn = ttk.Button(self.left_menu, text="Settings", command=open_settings)
        elif self.tab == "settings":
            self.editors_btn = ttk.Button(self.left_menu, text="Editors", command=open_editors)
            self.settings_btn = ttk.Button(self.left_menu, text="Settings", state="disabled")

        self.editors_btn.grid(row=0, column=0, pady=1, padx=20, sticky="nsew")
        self.settings_btn.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")

    def create_footer(self):
        # self.create_label(self.left_menu, f'hub {self.version}', 3)
        self.create_label(self.left_menu, "Ryan Zmuda © 2024", 4)
        self.create_label(self.left_menu, "Licensed under the MIT license.", 5)
        self.create_report_problem_label()

    def create_label(self, parent, text, row):
        label = tk.Label(parent, text=text)
        label.grid(row=row, column=0, pady=(0, 5), padx=20, sticky="sew")

    def create_report_problem_label(self):
        def report_problem():
            webbrowser.open("https://github.com/yoyoengine/launcher/issues")

        report_label = tk.Label(self.left_menu, text="Report a problem", fg="cyan", cursor="hand2")
        report_label.grid(row=6, column=0, pady=(0, 20), padx=30, sticky="sew")
        report_label.bind("<Button-1>", lambda e: report_problem())

    def create_content_area(self):
        self.content_frame = tk.Frame(self.root, bg="#171617")
        self.content_frame.grid(row=1, column=1, sticky="nsew", pady=(0, 0))

        self.canvas = tk.Canvas(self.content_frame, bg="#171617", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#171617", padx=10, pady=10)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", self.update_scrollregion)
        self.canvas.bind("<Configure>", self.update_scrollregion)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfigure(self.canvas_window, width=event.width)

    def bind_mouse_events(self):
        def on_mouse_wheel(event):
            self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

        def on_mouse_wheel_linux(event):
            self.canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

        self.canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", on_mouse_wheel_linux)
        self.canvas.bind_all("<Button-5>", on_mouse_wheel_linux)

    def trim_version(self, version):
        return version.replace('_', ' ').replace('-', ' ')

    def populate_available_editors(self):
        # big text that says "Available:"
        available_label = tk.Label(self.scrollable_frame, text="Available:", bg="#171617", fg="white", font=("Roboto", 18))
        available_label.pack(fill="x", pady=10)

        try:
            remote_versions = self.backend.check_remote_versions()
            installed_versions = self.backend.check_installed_versions()
        except Exception as e:
            print("an exception has occurred:",e)
            remote_versions = []
            installed_versions = []

        # prune from remote_versions any versions that are already installed
        for installed_version in installed_versions:
            for remote_version in remote_versions:
                if installed_version['version'] == remote_version['version']:
                    remote_versions.remove(remote_version)

        if len(remote_versions) == 0:
            no_versions_label = tk.Label(self.scrollable_frame, text="No yoyoengine releases detected!", bg="#171617", fg="orange", font=("Roboto", 16))
            no_versions_label.pack(fill="x", pady=10)
        else:
            for version in remote_versions:
                version_frame = tk.Frame(self.scrollable_frame, bg="#1d1c1d", padx=10, pady=10)
                version_frame.pack(fill="x", pady=5)

                # Logo image label
                self.logo_label = tk.Label(version_frame, image=self.version_logo)
                self.logo_label.pack(side="left", padx=5)
                
                # Details frame to hold version details
                details_frame = tk.Frame(version_frame, bg="#1d1c1d")
                details_frame.pack(side="left", fill="x", expand=True)
                
                # Title label
                version_label = tk.Label(details_frame, text=f"{self.trim_version(version['version'])}", bg="#1d1c1d", fg="white", font=("Roboto", 16))
                version_label.pack(side="top", anchor="w")
                
                # Time ago label
                time_ago_label = tk.Label(details_frame, text=f"released {time_ago(version['date'])}", bg="#1d1c1d", fg="gray", font=("Roboto", 10))
                time_ago_label.pack(side="top", anchor="w")
                
                # Buttons frame
                buttons_frame = tk.Frame(details_frame, bg="#1d1c1d")
                buttons_frame.pack(side="top", anchor="w", pady=5)
                
                def install_handler(tag):
                    self.backend.install_by_tag(tag)
                    # asyncio.run(
                    self.notifier.send("YoyoEngine Hub", f"Editor: {version['version']} has been installed.", icon=Icon(name="../media/smallcleanlogo.png"))
                    # )
                    self.clear()
                    self.hub()

                install_button = ttk.Button(buttons_frame, text="Install", command=lambda version=version['version']: install_handler(version))
                install_button.pack(side="left", padx=5)
                
                release_notes_button = ttk.Button(buttons_frame, text="Release Notes", command=lambda url=version['url']: webbrowser.open(url))
                release_notes_button.pack(side="left", padx=5)

    def populate_installed_editors(self):
        # big text that says "Installed:"
        installed_label = tk.Label(self.scrollable_frame, text="Installed:", bg="#171617", fg="white", font=("Roboto", 18))
        installed_label.pack(fill="x", pady=10)

        versions = self.backend.check_installed_versions()

        if len(versions) == 0:
            no_versions_label = tk.Label(self.scrollable_frame, text="No yoyoengine installations detected!", bg="#171617", fg="orange", font=("Roboto", 16))
            no_versions_label.pack(fill="x", pady=10)
        else:
            for version in versions:
                version_frame = tk.Frame(self.scrollable_frame, bg="#1d1c1d", padx=10, pady=10)
                version_frame.pack(fill="x", pady=5)

                # Logo image label
                self.logo_label = tk.Label(version_frame, image=self.version_logo)
                self.logo_label.pack(side="left", padx=5)
                
                # Details frame to hold version details
                details_frame = tk.Frame(version_frame, bg="#1d1c1d")
                details_frame.pack(side="left", fill="x", expand=True)
                
                # Title label
                version_label = tk.Label(details_frame, text=f"{self.trim_version(version['version'])}", bg="#1d1c1d", fg="white", font=("Roboto", 16))
                version_label.pack(side="top", anchor="w")
                
                # Buttons frame
                buttons_frame = tk.Frame(details_frame, bg="#1d1c1d")
                buttons_frame.pack(side="top", anchor="w", pady=5)
                
                install_button = ttk.Button(buttons_frame, text="Open", command=lambda version=version: self.backend.open_editor(version))
                install_button.pack(side="left", padx=5)
                
                docs_button = ttk.Button(buttons_frame, text="Docs", command=lambda url="https://yoyoengine.github.io/docs/": webbrowser.open(url))
                docs_button.pack(side="left", padx=5)

                def handle_uninstall(version):
                    self.backend.uninstall_editor(version)
                    # asyncio.run(
                    self.notifier.send("YoyoEngine Hub", f"Editor: {version['version']} has been uninstalled.", icon=Icon(name="../media/smallcleanlogo.png"))
                    # )
                    self.clear()
                    self.hub()

                uninstall_button = ttk.Button(buttons_frame, text="Uninstall", command=lambda version=version: handle_uninstall(version))
                uninstall_button.pack(side="left", padx=5)

    def populate_editors_tab(self):
        self.populate_installed_editors()
        self.populate_available_editors()

    def populate_settings_tab(self):
        label = tk.Label(self.scrollable_frame, text="Settings", bg="#171617", fg="white", font=("Roboto", 18))
        label.pack(fill="x", pady=10)

        # uninstall everything
        def uninstall_all():
            self.backend.uninstall_everything()
            self.notifier.send("YoyoEngine Hub", "All editors have been uninstalled.", icon=Icon(name="../media/smallcleanlogo.png"))
            self.clear()
            self.hub()
        
        uninstall_button = tk.Button(self.scrollable_frame, text="Uninstall All", command=uninstall_all, bg="#ff0000", fg="white")
        uninstall_button.pack(pady=10)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def configure_grid(self, parent, columns, rows):
        for col in columns:
            parent.grid_columnconfigure(col, weight=1)
        for row in rows:
            parent.grid_rowconfigure(row, weight=1)

    def run(self):
        sv_ttk.set_theme("dark")
        self.root.mainloop()