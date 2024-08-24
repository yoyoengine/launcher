"""
    This file is a part of yoyoengine. (https://github.com/zoogies/yoyoengine)
    Copyright (C) 2024  Ryan Zmuda

    Licensed under the MIT license. See LICENSE file in the project root for details.
"""

import tkinter as tk
from tkinter import ttk
import sv_ttk
import webbrowser
from backend import YoyoEngineHubBackend
from desktop_notifier import DesktopNotifier

class YoyoEngineHub:
    def __init__(self, version):
        self.notifier = DesktopNotifier()
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("YoyoEngine Hub")
        self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file='../media/cleanlogo.png'))
        self.tab = "editors"
        self.backend = YoyoEngineHubBackend(version)
        self.update_available = self.backend.check_for_hub_update()

        if self.update_available:
            self.show_update_notification()
        else:
            self.platform = self.backend.platform
            if self.platform != "Linux":
                self.show_platform_error()
            else:
                self.hub()
                print(self.backend.check_installed_versions())

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

    def configure_root_grid(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=20)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)

    def create_top_bar(self):
        self.top_bar = tk.Frame(self.root)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.top_bar.columnconfigure(0, weight=1)
        self.logo = tk.PhotoImage(file="../media/smallesttextlogo.png")
        self.logo_label = tk.Label(self.top_bar, image=self.logo)
        self.logo_label.grid(row=0, column=0, pady=0, padx=10, sticky="nw")

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
        self.create_label(self.left_menu, "Ryan Zmuda © 2024", 3)
        self.create_label(self.left_menu, "Licensed under the MIT license.", 4)
        self.create_report_problem_label()

    def create_label(self, parent, text, row):
        label = tk.Label(parent, text=text)
        label.grid(row=row, column=0, pady=(0, 5), padx=20, sticky="sew")

    def create_report_problem_label(self):
        def report_problem():
            webbrowser.open("https://github.com/yoyoengine/launcher/issues")

        report_label = tk.Label(self.left_menu, text="Report a problem", fg="cyan", cursor="hand2")
        report_label.grid(row=5, column=0, pady=(0, 20), padx=30, sticky="sew")
        report_label.bind("<Button-1>", lambda e: report_problem())

    def create_content_area(self):
        self.content_frame = tk.Frame(self.root, bg="#171617")
        self.content_frame.grid(row=1, column=1, sticky="nsew", pady=(0, 0))

        self.canvas = tk.Canvas(self.content_frame, bg="#171617")
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

    def populate_editors_tab(self):
        versions = self.backend.check_installed_versions()
        for version in versions:
            version_frame = tk.Frame(self.scrollable_frame, bg="#282828", padx=10, pady=10)
            version_frame.pack(fill="x", pady=5)
            version_label = tk.Label(version_frame, text=f"Version: {version}", bg="#282828", fg="white")
            version_label.pack(side="left", fill="x", expand=True)

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