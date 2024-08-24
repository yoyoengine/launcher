"""
    This file is a part of yoyoengine. (https://github.com/zoogies/yoyoengine)
    Copyright (C) 2024  Ryan Zmuda

    Licensed under the MIT license. See LICENSE file in the project root for details.
"""

import tkinter as tk
from tkinter import ttk, Frame
from desktop_notifier import DesktopNotifier, Icon

import asyncio

import sv_ttk

import backend


class YoyoEngineHub:
    def __init__(self, version):

        self.notifier = DesktopNotifier()
        # asyncio.run(self.notifier.send(title="YoyoEngine Hub", message="Welcome to YoyoEngine Hub!", icon="../media/cleanlogo.png"))

        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("YoyoEngine Hub")
        self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file='../media/cleanlogo.png'))

        self.tab = "editors"

        self.backend = backend.YoyoEngineHubBackend(version)

        self.update_available = self.backend.check_for_hub_update()
        if(self.update_available):
            url = "https://github.com/yoyoengine/launcher/releases/latest"
            
            def open_update():
                # open the browser to the latest release
                import webbrowser
                webbrowser.open(url)
            
            def ignore_update():
                self.update_available = False
                self.clear()
                self.hub() # TODO

            notification_label = ttk.Label(self.root, text="An update is available!", font=("Roboto", 16))
            notification_label.grid(row=0, column=0, columnspan=2, pady=10)

            ignore_button = ttk.Button(self.root, text="Ignore", width=50, command=ignore_update)
            ignore_button.grid(row=1, column=0, padx=5, pady=5)

            install_button = ttk.Button(self.root, text="Install", width=50, command=open_update)
            install_button.grid(row=1, column=1, padx=5, pady=5)

            self.root.grid_columnconfigure(0, weight=1)
            self.root.grid_columnconfigure(1, weight=1)
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_rowconfigure(1, weight=1)

        else:
            self.platform = self.backend.platform
            if(self.platform != "Linux"):
                self.clear()

                self.frame3 = Frame(self.root, width=300, height=300)
                self.frame3.pack()
                self.error_txt = ttk.Label(self.frame3, text='This program only works on Linux.')
                self.error_txt.pack()
            else:
                self.hub()

                print(self.backend.check_installed_versions())

    def clear(self):
        for i in self.root.winfo_children():
            i.destroy()

    def hub(self):
        self.clear()
    
        # Configure root window grid
        self.root.columnconfigure(0, weight=1)  # Sidebar column (20% width)
        self.root.columnconfigure(1, weight=20)  # Main content column (80% width)
        self.root.rowconfigure(0, weight=0)  # Top bar row
        self.root.rowconfigure(1, weight=1)  # Main content row
    
        # Top bar container
        self.top_bar = tk.Frame(self.root)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.top_bar.columnconfigure(0, weight=1)
    
        # Logo image in the top bar
        self.logo = tk.PhotoImage(file="../media/smallesttextlogo.png")
        self.logo_label = tk.Label(self.top_bar, image=self.logo)
        self.logo_label.grid(row=0, column=0, pady=0, padx=10, sticky="nw")
    
        # Left menu container
        self.left_menu = tk.Frame(self.root)
        self.left_menu.grid(row=1, column=0, sticky="nsew")
        self.left_menu.columnconfigure(0, weight=1)  # Ensure buttons fill the width
        self.left_menu.rowconfigure(2, weight=1)  # Ensure bottom labels are aligned to the bottom
    
        def open_editors():
            self.tab = "editors"
            self.clear()
            self.hub()
        
        def open_settings():
            self.tab = "settings"
            self.clear()
            self.hub()

        # Sidebar buttons in the left menu
        if(self.tab == "editors"):
            self.editors_btn = ttk.Button(self.left_menu, text="Editors", state="disabled")
            self.editors_btn.grid(row=0, column=0, pady=1, padx=20, sticky="nsew")
            self.settings_btn = ttk.Button(self.left_menu, text="Settings", command=open_settings)
            self.settings_btn.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")
        elif (self.tab == "settings"):
            self.editors_btn = ttk.Button(self.left_menu, text="Editors", command=open_editors)
            self.editors_btn.grid(row=0, column=0, pady=1, padx=20, sticky="nsew")
            self.settings_btn = ttk.Button(self.left_menu, text="Settings", state="disabled")
            self.settings_btn.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")
    
        # Main content area
        self.content_frame = tk.Frame(self.root, bg="#171617")
        self.content_frame.grid(row=1, column=1, sticky="nsew", pady=(0, 0))
    
        # Copyright label
        self.copyright_label = tk.Label(self.left_menu, text="Ryan Zmuda © 2024")
        self.copyright_label.grid(row=3, column=0, pady=(0, 5), padx=20, sticky="sew")
    
        self.copyright_label = tk.Label(self.left_menu, text="Licensed under the MIT license.")
        self.copyright_label.grid(row=4, column=0, pady=(0, 5), padx=20, sticky="sew")
    
        def report_problem():
            # open issues in browser for yoyoengine/launcher
            import webbrowser
            webbrowser.open("https://github.com/yoyoengine/launcher/issues")
    
        # Report problem label
        self.report_label = tk.Label(self.left_menu, text="Report a problem", fg="cyan", cursor="hand2")
        self.report_label.grid(row=5, column=0, pady=(0, 20), padx=30, sticky="sew")
        self.report_label.bind("<Button-1>", lambda e: report_problem())
    
        if self.tab == "editors":
            pass
        else:
            pass

    def run(self):
        sv_ttk.set_theme("dark")
        self.root.mainloop()